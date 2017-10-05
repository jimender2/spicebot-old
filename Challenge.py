import sopel
from sopel import module, tools
import random
import os
from os.path import exists
from random import randint
import time

script_dir = os.path.dirname(__file__)
rel_path = "data/weapons.txt"
weaponslocker = os.path.join(script_dir, rel_path)

TIMEOUT = 300

## React to /me challenges
@module.rule('^(?:challenges|(?:fi(?:ght|te)|duel)s(?:\s+with)?)\s+([a-zA-Z0-9\[\]\\`_\^\{\|\}-]{1,32}).*')
@module.intent('ACTION')
@module.require_chanmsg
def challenge_action(bot, trigger):
    return challenge(bot, trigger.sender, trigger.nick, trigger.group(1))

################
## Challenges ##
################

@sopel.module.commands('challenge','duel')
@module.require_chanmsg
def challenge_cmd(bot, trigger):
    return challenge(bot, trigger.sender, trigger.nick, trigger.group(3) or '')

def challenge(bot, channel, instigator, target):
    target = tools.Identifier(target or '')
    if not target:
        bot.say(instigator + ", Who did you want to fight?")
    else:
        ## Don't allow instigator to challenge if he has fought recently
        instigatortime = time_since_challenge(bot, instigator)
        targettime = time_since_challenge(bot, target)
        ## People can opt out of playing
        instigatordisenable = get_challengestatus(bot, instigator)
        targetdisenable = get_challengestatus(bot, target)
        ## Here We Go!
        if target == bot.nick:
            bot.say("I refuse to fight a biological entity!")
        elif target == instigator:
            bot.say("If you are feeling self-destructive, there are places you can call.")
        elif target.lower() not in bot.privileges[channel.lower()]:
            bot.say("I'm not sure who that is.")
        elif instigatortime < TIMEOUT and bot.nick.endswith('dev'):
            bot.notice("You can't challenge for %d seconds." % (TIMEOUT - instigatortime), instigator)
            if targettime < TIMEOUT:
                bot.notice(target + " can't challenge for %d seconds." % (TIMEOUT - targettime), instigator)
        elif targettime < TIMEOUT and bot.nick.endswith('dev'):
            bot.notice(target + " can't challenge for %d seconds." % (TIMEOUT - targettime), instigator)
        elif instigatordisenable:
            bot.say(instigator + ', It looks like you have disabled Challenges. Run .challengeon to re-enable.')
        elif targetdisenable:
            bot.say(instigator + ', It looks like ' + target + ' has disabled Challenges.')
        else:
            ## Announce
            bot.say(instigator + " versus " + target)
            ## Random Health potion
            healthpotion = randomhealthpotion()
            if healthpotion == 'true':
                bot.say(instigator + ' found a health potion worth 100 health. Use .challengehealthpotion to consume.')
                addhealthpotion(bot, instigator)
            ## Weapon, damage done. 
            weapon = weaponofchoice()
            damage = damagedone(bot)
            ## Select Winner
            winner, loser = getwinner(bot, instigator, target)
            bot.say(winner + " wins!")
            ## Update wins/lose
            update_wins(bot, winner)
            update_losses(bot, loser)
            ## Update XP,,, XPearned = damagedone + 1
            XPearned = str(int(damage) + 1)
            update_xp(bot, winner, XPearned)
            ## check if new player health not set
            update_spawn(bot, winner)
            update_spawn(bot, loser)
            ## Update health, If killed, respawn
            currenthealth = update_health(bot, loser, damage)
            if currenthealth <= 0:
                bot.say(winner + ' killed ' + loser + " with " + weapon + ' forcing a respawn!!')
                update_respawn(bot, loser)
                ## Loot Corpse
                stealhealthpotions = loothealthpotions(bot, loser, winner)
            else:
                bot.say(winner + " hits " + loser + " with " + weapon + ', dealing ' + damage + ' damage.')
            ## Update Time of combat
            now = time.time()
            targetnow = (int(now) + 180)
            update_time(bot, instigator, now)
            update_time(bot, target, targetnow)
       
###################
## Winner / Loser ##
###################

def getwinner(bot, instigator, target):
    instigatorxp = get_xp(bot, instigator)
    targetxp = get_xp(bot, target)
    if instigatorxp == targetxp:
        combatants = sorted([instigator, instigator, instigator, target, target])
    elif instigatorxp > targetxp:
        combatants = sorted([instigator, instigator, instigator, instigator, target, target])
    elif instigatorxp < targetxp:
        combatants = sorted([instigator, instigator, instigator, target, target, target])
    else:
        combatants = sorted([instigator, instigator, target, target, target])
    random.shuffle(combatants)
    winner = combatants.pop()
    if winner == instigator:
        loser = target
    else:
        loser = instigator
    return winner, loser

def get_wins(bot, nick):
    wins = bot.db.get_nick_value(nick, 'challenges_wins') or 0
    return wins

def update_wins(bot, nick):
    wins = get_wins(bot, nick)
    bot.db.set_nick_value(nick, 'challenges_wins', wins + 1)

def get_losses(bot, nick):
    losses = bot.db.get_nick_value(nick, 'challenges_losses') or 0
    return losses

def update_losses(bot, nick):
    losses = get_losses(bot, nick)
    bot.db.set_nick_value(nick, 'challenges_losses', losses + 1)
    
@sopel.module.require_admin
@module.require_chanmsg
@module.commands('challengewinslossclear')
def challengewinslossclear(bot, trigger):
    target = trigger.group(3) or trigger.nick
    ## Wins
    wins = get_wins(bot, target)
    if wins:
        bot.db.set_nick_value(target, 'challenges_wins', '')
    ## Losses
    losses = get_losses(bot, target)
    if losses:
        bot.db.set_nick_value(target, 'challenges_losses', '')
    bot.say(target + "'s wins and losses have been cleared.")
    
############
## Health ##
############

def get_health(bot, nick):
    health = bot.db.get_nick_value(nick, 'challenges_health') or 0
    return health

def update_health(bot, nick, damage):
    health = get_health(bot, nick)
    if not health:
        update_respawn(bot, nick)
    bot.db.set_nick_value(nick, 'challenges_health', (int(health) - int(damage)))
    currenthealth = get_health(bot, nick)
    return currenthealth

@sopel.module.require_admin
@module.require_chanmsg
@module.commands('challengehealthclear')
def challengehealthclear(bot, trigger):
    target = trigger.group(3) or trigger.nick
    ## health
    health = get_health(bot, target)
    if health:
        bot.db.set_nick_value(target, 'challenges_health', '1')
    bot.say(target + "'s health has been cleared.")

#################
## Damage Done ##
#################

def damagedone(bot):
    rando = randint(1, 100)
    if rando >= 90:
        damage = '120'
    elif rando >= 75 and rando < 90:
        damage = '70'
    elif rando < 75 and rando > 10:
        damage = '40'
    elif rando > 1 and rando <= 10:
        damage = '10'    
    else:
        damage = '5'
        bot.say('rando: ' + str(rando) + ' damage: ' + str(damage))
    return damage

####################
## Health Potions ##
####################

def loothealthpotions(bot, loser, winner):
    loserhealthpotions = get_healthpotions(bot, loser)
    if loserhealthpotions:
        bot.db.set_nick_value(loser, 'challenges_healthpotions', '')
        winnerhealthpotions = get_healthpotions(bot, winner)
        bot.db.set_nick_value(winner, 'challenges_healthpotions', int(winnerhealthpotions) + int(loserhealthpotions))
            
def get_healthpotions(bot, nick):
    healthpotions = bot.db.get_nick_value(nick, 'challenges_healthpotions') or 0
    return healthpotions

def addhealthpotion(bot, nick):
    healthpotions = get_healthpotions(bot, nick)
    bot.db.set_nick_value(nick, 'challenges_healthpotions', int(healthpotions) + 1)

def randomhealthpotion():
    randomhealthchance = randint(1, 120)
    if randomhealthchance >= 90:
        healthpotion = 'true'
    else:
        healthpotion = 'false'
    return healthpotion

@module.require_chanmsg
@module.commands('challengehealthpotion')
def usehealthpotion(bot, trigger):
    target = trigger.group(3) or trigger.nick
    healthpotions = get_healthpotions(bot, trigger.nick)
    if healthpotions:
        health = get_health(bot, target)
        if target == trigger.nick:
            bot.say(trigger.nick + ' uses health potion.')
        else:
            bot.say(trigger.nick + ' uses health potion on ' + target + ".")
        bot.db.set_nick_value(target, 'challenges_health', int(health) + 100)
        bot.db.set_nick_value(trigger.nick, 'challenges_healthpotions', int(healthpotions) - 1)
    else:
        bot.say('You do not have a healthpotion to use!')

@sopel.module.require_admin
@module.require_chanmsg
@module.commands('challengehealthpotiongive')
def challengehealthpotiongive(bot, trigger):
    target = trigger.group(3) or trigger.nick
    addhealthpotion(bot, target)
    bot.say(target + ' now has a health potion.')
    
@sopel.module.require_admin
@module.require_chanmsg
@module.commands('challengehealthpotiontake')
def challengehealthpotiontake(bot, trigger):
    target = trigger.group(3) or trigger.nick
    bot.db.set_nick_value(target, 'challenges_healthpotions', '')
    bot.say(target + ' now has no healthpotions.')

#############
## Respawn ##
#############
 
def get_respawn(bot, nick):
    respawns = bot.db.get_nick_value(nick, 'challenges_respawns') or 0
    return respawns

def update_respawn(bot, nick):
    respawns = get_respawn(bot, nick)
    bot.db.set_nick_value(nick, 'challenges_respawns', respawns + 1)
    bot.db.set_nick_value(nick, 'challenges_health', '1000')
    currentrespawns = get_respawn(bot, nick)
    return currentrespawns

def update_spawn(bot, nick):
    health = get_health(bot, nick)
    if not health:
        bot.db.set_nick_value(nick, 'challenges_health', '1000')

@sopel.module.require_admin
@module.require_chanmsg
@sopel.module.commands('challengerespawnclearall')
def challengerespawnclearall(bot, trigger):
    return challengerespawnallclear(bot, trigger.sender)

def challengerespawnallclear(bot, channel):
    bot.say('resetting respawns for the channel')
    for u in bot.channels[channel].users:
            target = u
            respawns = get_respawn(bot, target)
            if respawns:
                bot.db.set_nick_value(target, 'challenges_respawns', '')

########
## XP ##
########

def get_xp(bot, nick):
    xp = bot.db.get_nick_value(nick, 'challenges_xp') or 0
    return xp

def update_xp(bot, nick, damage):
    xp = get_xp(bot, nick)
    bot.db.set_nick_value(nick, 'challenges_xp', xp + int(damage))
    currentxp = get_xp(bot, nick)
    return currentxp

@sopel.module.require_admin
@module.require_chanmsg
@module.commands('challengexpclear')
def challengexpclear(bot, trigger):
    target = trigger.group(3) or trigger.nick
    ## XP
    xp = get_xp(bot, target)
    if xp:
        bot.db.set_nick_value(target, 'challenges_xp', '')
    bot.say(target + "'s XP has been cleared.")
    
#############
## Weapons ##
#############

@module.require_chanmsg
@sopel.module.commands('weaponslocker')
def weaponslockercmd(bot, trigger):
    bot.say('Use weaponslockeradd or weaponslockerdel to adjust Locker Inventory.')

@module.require_chanmsg
@sopel.module.commands('weaponslockeradd')
def addweapons(bot, trigger):
    checkweapons()
    if not trigger.group(2):
        bot.say("what weapon would you like to add?")
    else:
        weaponnew = str(trigger.group(2))
        if str(weaponnew) in open(weaponslocker).read():
            bot.say(weaponnew + " is already in the weapons locker.")
        else:
            with open(weaponslocker, "a") as myfile:
                myfile.write("\n")
                myfile.write(weaponnew)
            if str(weaponnew) in open(weaponslocker).read():
                bot.say(weaponnew + " has been added to the weapons locker.")

def checkweapons():
    if not exists(weaponslocker):
        createweapons()
    if os.stat(weaponslocker).st_size == 0:
        createweapons()
     
def createweapons():
    weapons  = ["waffle-iron","fish","knuckle-sandwich","sticky-note","blender","hammer","nailgun","rotisserie chicken","steel-toed boot","stapler"]
    for w in weapons:
        with open(weaponslocker, "a") as myfile:
            if os.stat(weaponslocker).st_size != 0:
                myfile.write("\n")
            myfile.write(w)

@module.require_chanmsg
@sopel.module.commands('weaponslockerdel')
def removeweapons(bot, trigger):
    checkweapons()
    if not trigger.group(2):
        bot.say("what weapon would you like to remove?")
    else:
        weapondel = str(trigger.group(2))
        if str(weapondel) in open(weaponslocker).read():
            os.system('sudo sed -i "/' + str(weapondel) + '/d; /^$/d" ' + weaponslocker)
            if str(weapondel) not in open(weaponslocker).read():
                bot.say(weapondel + ' has been removed from the weapons locker.')
        else:
            bot.say(weapondel + " is not in the weapons locker.")

def weaponofchoice():
    checkweapons()
    weapons = open(weaponslocker).read().splitlines()
    weapon =random.choice(weapons)
    if weapon.startswith('a') or weapon.startswith('e') or weapon.startswith('i') or weapon.startswith('o') or weapon.startswith('u'):
        weapon = str('an ' + weapon)
    else:
        weapon = str('a ' + weapon)
    return weapon

##########
## Time ##
##########

def update_time(bot, nick, now):
    bot.db.set_nick_value(nick, 'challenge_last', now)
    
def time_since_challenge(bot, nick):
    now = time.time()
    last = bot.db.get_nick_value(nick, 'challenge_last') or 0
    return abs(now - last)

@sopel.module.require_admin
@module.require_chanmsg
@module.commands('challengetimeclear')
def challengetimeclear(bot, trigger):
    target = trigger.group(3) or trigger.nick
    ## TIMEOUT
    time_since = time_since_challenge(bot, target)
    if time_since:
        bot.db.set_nick_value(target, 'challenge_last', '')
    bot.say(target + "'s time has been cleared.")

@sopel.module.require_admin
@module.require_chanmsg
@sopel.module.commands('challengetimeclearall')
def challenge_timeall(bot, trigger):
    return challengealltimeclear(bot, trigger.sender)

def challengealltimeclear(bot, channel):
    for u in bot.channels[channel].users:
            target = u
            time_since = time_since_challenge(bot, target)
            if time_since:
                bot.db.set_nick_value(target, 'challenge_last', '')

###########
## Stats ##
###########

@module.require_chanmsg
@module.commands('challenges','duels')
def challenges(bot, trigger):
    target = trigger.group(3) or trigger.nick
    stats = ''
    ## health
    health = get_health(bot, target)
    if health:
        addstat = str(" Health=" + str(health) + ".")
        stats = str(stats + addstat)
    ## XP
    xp = get_xp(bot, target)
    if xp:
        addstat = str(" XP=" + str(xp) + ".")
        stats = str(stats + addstat)
    ## Wins
    wins = get_wins(bot, target)
    if wins:
        addstat = str(" Wins=" + str(wins) + ".")
        stats = str(stats + addstat)
    ## Losses
    losses = get_losses(bot, target)
    if losses:
        addstat = str(" Lost=" + str(losses) + ".")
        stats = str(stats + addstat)
    ## Respawns
    respawnamount = get_respawn(bot, target)
    if respawnamount:
        addstat = str(" Respawns=" + str(respawnamount) + ".")
        stats = str(stats + addstat)
    ## TIMEOUT
    time_since = time_since_challenge(bot, target)
    if time_since < TIMEOUT:
        timediff = int(TIMEOUT - time_since)
        addstat = str(" TIMEOUT=" + str(timediff) + ".")
        stats = str(stats + addstat)
    ## Inventory
    howmanyhealthpotions = get_healthpotions(bot, target)
    if howmanyhealthpotions:
        addstat = str(" HealthPotions=" + str(howmanyhealthpotions) + ".")
        stats = str(stats + addstat)
    
    if stats != '':
        stats = str(target + "'s stats:" + stats)
        bot.say(stats)
    else:
        bot.say(target + ' has no stats.')

@sopel.module.require_admin
@module.require_chanmsg
@module.commands('challengeallstatsclear')
def challengestatsclear(bot, trigger):
    target = trigger.group(3) or trigger.nick
    ## Wins
    wins = get_wins(bot, target)
    if wins:
        bot.db.set_nick_value(target, 'challenges_wins', '')
    ## Losses
    losses = get_losses(bot, target)
    if losses:
        bot.db.set_nick_value(target, 'challenges_losses', '')
    ## health
    health = get_health(bot, target)
    if health:
        bot.db.set_nick_value(target, 'challenges_health', '1000')
    ## XP
    xp = get_xp(bot, target)
    if xp:
        bot.db.set_nick_value(target, 'challenges_xp', '')
    ## TIMEOUT
    time_since = time_since_challenge(bot, target)
    if time_since:
        bot.db.set_nick_value(target, 'challenge_last', '')
    
    bot.say(target + "'s stats have been cleared.")
    
####################
## Enable/Disable ##
####################

def get_challengestatus(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'challenges_disenable') or 0
    return disenable

@module.require_chanmsg
@module.commands('challengeon','duelon')
def challengeon(bot, trigger):
    target = trigger.group(3) or trigger.nick
    if not trigger.admin and target != trigger.nick:
        bot.say("Only bot admins can mark other users as able to challenge.")
    else:
        disenable = get_challengestatus(bot, target)
        if disenable:
            bot.db.set_nick_value(target, 'challenges_disenable', '')
            bot.say('Challenges has been enabled for ' + target)
        else:
            bot.say('Challenges are already enabled for ' + target)

@module.require_chanmsg
@module.commands('challengeoff','dueloff')
def challengeoff(bot, trigger):
    target = trigger.group(3) or trigger.nick
    if not trigger.admin and target != trigger.nick:
        bot.say("Only bot admins can mark other users as not able to challenge.")
    else:
        disenable = get_challengestatus(bot, target)
        if disenable:
            bot.say('Challenges are already disabled for ' + target)
        else:
            bot.db.set_nick_value(target, 'challenges_disenable', 'true')
            bot.say('Challenges has been disabled for ' + target)

#############
## streaks ##
#############

