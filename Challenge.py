import sopel
from sopel import module, tools
import random
from random import randint
import time
import sys, re
import os
from os.path import exists

moduledir = os.path.dirname(__file__)
relativepath = "data/weapons.txt"
weaponslocker = os.path.join(moduledir, relativepath)

TIMEOUT = 180
TIMEOUTC = 40
ALLCHAN = 'entirechannel'
OPTTIMEOUT = 3600

## React to /me (ACTION) challenges
@module.rule('^(?:challenges|(?:fi(?:ght|te)|duel)s(?:\s+with)?)\s+([a-zA-Z0-9\[\]\\`_\^\{\|\}-]{1,32}).*')
@module.intent('ACTION')
@module.require_chanmsg
def challenge_action(bot, trigger):
    instigator = trigger.nick
    target = trigger.nick
    targetdisenable = get_spicebotdisenable(bot, target)
    if targetdisenable:
        return challenge(bot, trigger.sender, trigger.nick, trigger.group(1))
    else:
        instigator = trigger.nick
        warned = bot.db.get_nick_value(target, 'spicebothour_warn') or 0
        if not warned:
            bot.notice(target + ", you have to run .spiceboton to allow her to listen to you.", instigator)
        else:
            bot.notice(target + ", it looks like your access to spicebot has been disabled for a while. Check out ##SpiceBotTest.", instigator)
        
####################
## Main Operation ##
####################

@sopel.module.commands('challenge','duel')
@module.require_chanmsg
def challenge_cmd(bot, trigger):
    instigator = trigger.nick
    target = trigger.nick
    targetdisenable = get_spicebotdisenable(bot, target)
    if targetdisenable:
        return challenge(bot, trigger.sender, trigger.nick, trigger.group(3) or '')
    else:
        instigator = trigger.nick
        warned = bot.db.get_nick_value(target, 'spicebothour_warn') or 0
        if not warned:
            bot.notice(target + ", you have to run .spiceboton to allow her to listen to you.", instigator)
        else:
            bot.notice(target + ", it looks like your access to spicebot has been disabled for a while. Check out ##SpiceBotTest.", instigator)
        
def challenge(bot, channel, instigator, target):
    target = tools.Identifier(target or '')
    if not target:
        bot.notice(instigator + ", Who did you want to fight?", instigator)
    else:
        
        ## Don't allow chat spamming
        instigatortime = get_timesince(bot, instigator)
        targettime = get_timesince(bot, target)
        channeltime = get_timesince(bot, ALLCHAN)
        
        ## Bot opt-out
        instigatorspicebotdisenable = get_spicebotdisenable(bot, instigator)
        targetspicebotdisenable = get_spicebotdisenable(bot, target)
        if not instigatorspicebotdisenable:
            sys.exit()
        if not targetspicebotdisenable:
            sys.exit()
        
        ## People can opt out of playing
        instigatordisenable = get_disenable(bot, instigator)
        targetdisenable = get_disenable(bot, target)
        
        ## Non-Duel Interactions
        if target == bot.nick:
            bot.say("I refuse to fight a biological entity!")
        elif target == instigator:
            bot.say("If you are feeling self-destructive, there are places you can call.")
        elif target.lower() not in bot.privileges[channel.lower()]:
            bot.say("I'm not sure who that is.")
        
        ## Check Opt-in Status
        elif not instigatordisenable:
            bot.notice(instigator + ", It looks like you have disabled Challenges. Run .challengeon to re-enable.", instigator)
        elif not targetdisenable:
            bot.notice(instigator + ', It looks like ' + target + ' has disabled Challenges.', instigator)
        
        ## Enforce Timeout, unless in dev-channel
        elif instigatortime < TIMEOUT and not bot.nick.endswith('dev'):
            bot.notice("You can't challenge for %d seconds." % (TIMEOUT - instigatortime), instigator)
            if targettime < TIMEOUT:
                bot.notice(target + " can't challenge for %d seconds." % (TIMEOUT - targettime), instigator)
            if channeltime < TIMEOUTC:
                bot.notice(channel + " can't challenge for %d seconds." % (TIMEOUTC - channeltime), instigator)
        elif targettime < TIMEOUT and not bot.nick.endswith('dev'):
            bot.notice(target + " can't challenge for %d seconds." % (TIMEOUT - targettime), instigator)
            if channeltime < TIMEOUTC:
                bot.notice(channel + " can't challenge for %d seconds." % (TIMEOUTC - channeltime), instigator)
        elif channeltime < TIMEOUTC and not bot.nick.endswith('dev'):
            bot.notice(channel + " can't challenge for %d seconds." % (TIMEOUTC - channeltime), instigator)
        
        ## If target and intigator pass the criteria above continue
        else:
        
            ## Announce Combat
            bot.say(instigator + " versus " + target)
            
            ## Check new player health, initial Spawn
            update_spawn(bot, instigator)
            update_spawn(bot, target)
            
############## Random Inventory gain,,,, right now just healthpotions
            randominventoryfind = randominventory()
            if randominventoryfind == 'true':
                loot, loot_text = determineloottype(bot, instigator)
                bot.say(instigator + ' found a ' + str(loot) + ' ' + str(loot_text))
            
            ## Weapon Select
            weapon = weaponofchoice(bot)
            
            ## Damage Done
            damage = damagedone(bot)

            ## Select Winner
            winner, loser = getwinner(bot, instigator, target)
            
            ## Update Wins and Losses
            update_wins(bot, winner)
            update_losses(bot, loser)
            
            ## Update XP points
            XPearnedwinner = '5'
            XPearnedloser = '3'
            update_xp(bot, winner, XPearnedwinner)
            update_xp(bot, loser, XPearnedloser)
            
            ## Update Health Of Loser, respawn, allow winner to loot
            currenthealth = update_health(bot, loser, damage)
            if currenthealth <= 0:
                bot.say(winner + ' killed ' + loser + " with " + weapon + ' forcing a respawn!!')
                update_respawn(bot, loser)
                ## Loot Corpse
                lootcorpse(bot, loser, winner)
            else:
                bot.say(winner + " hits " + loser + " with " + weapon + ', dealing ' + damage + ' damage.')
            
            ## Update Time Of Combat
            update_time(bot, instigator)
            update_time(bot, target)
            update_time(bot, ALLCHAN)

#############
## Opt Out ##
#############

## Enable
@module.require_chanmsg
@module.commands('challengeon','duelon','challengeoff','dueloff')
def challengeoptchange(bot, trigger):
    instigator = trigger.nick
    target = trigger.nick
    targetdisenable = get_spicebotdisenable(bot, target)
    if targetdisenable:
        command = trigger.group(1)
        channel = trigger.sender
        target = trigger.group(3) or trigger.nick
        if not trigger.admin and target != trigger.nick:
            bot.notice(instigator + ', Only bot admins can mark other users as not able to challenge."', instigator)
        elif target.lower() not in bot.privileges[channel.lower()]:
            bot.say("I'm not sure who that is.")
        disenable = get_disenable(bot, target)
        opttime = get_opttimeout(bot, target)
        if opttime < OPTTIMEOUT and not bot.nick.endswith('dev'):
            bot.notice(target + " can't enable/disable challenges for %d seconds." % (OPTTIMEOUT - opttime), instigator)
        elif not disenable:
            if command.endswith('on'):
                bot.db.set_nick_value(target, 'challenges_disenable', 'true')
                bot.say('Challenges has been enabled for ' + target)
                set_opttimeout(bot, target)
            elif command.endswith('off'):
                bot.say('Challenges are already disabled for ' + target)
        else:
            if command.endswith('on'):
                bot.say('Challenges are already enabled for ' + target)
            elif command.endswith('off'):
                bot.db.set_nick_value(target, 'challenges_disenable', '')
                bot.say('Challenges has been disabled for ' + target)
                set_opttimeout(bot, target)
            
    else:
        instigator = trigger.nick
        warned = bot.db.get_nick_value(target, 'spicebothour_warn') or 0
        if not warned:
            bot.notice(target + ", you have to run .spiceboton to allow her to listen to you.", instigator)
        else:
            bot.notice(target + ", it looks like your access to spicebot has been disabled for a while. Check out ##SpiceBotTest.", instigator)

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'challenges_disenable') or 0
    return disenable

## Check Status of Opt In
def get_spicebotdisenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable

##########
## Time ##
##########

def update_time(bot, nick):
    now = time.time()
    bot.db.set_nick_value(nick, 'challenges_time', now)
    
def get_timesince(bot, nick):
    now = time.time()
    last = bot.db.get_nick_value(nick, 'challenges_time') or 0
    return abs(now - last)

def get_timeout(bot, nick):
    time_since = get_timesince(bot, nick)
    if time_since < TIMEOUT:
        timediff = int(TIMEOUT - time_since)
    else:
        timediff = 0
    return timediff

def get_opttimeout(bot, nick):
    now = time.time()
    last = bot.db.get_nick_value(nick, 'challengesopt_time') or 0
    return abs(now - last)

def set_opttimeout(bot, nick):
    now = time.time()
    bot.db.set_nick_value(nick, 'challengesopt_time', now)
    
#####################
## Spawn / ReSpawn ##
#####################

def get_respawns(bot, nick):
    respawns = bot.db.get_nick_value(nick, 'challenges_respawns') or 0
    return respawns

def update_respawn(bot, nick):
    respawns = get_respawns(bot, nick)
    bot.db.set_nick_value(nick, 'challenges_respawns', respawns + 1)
    bot.db.set_nick_value(nick, 'challenges_health', '1000')
    currentrespawns = get_respawns(bot, nick)
    return currentrespawns

def update_spawn(bot, nick):
    health = get_health(bot, nick)
    if not health or int(health) <= 0:
        bot.db.set_nick_value(nick, 'challenges_health', '1000')

###############
## Inventory ##
###############

## maybe add a dice roll later
def randominventory():
    randomfindchance = randint(1, 120)
    if randomfindchance >= 90:
        randominventoryfind = 'true'
    else:
        randominventoryfind = 'false'
    return randominventoryfind

def determineloottype(bot, instigator):
    typesofloot  = ["healthpotion","healthpotion","healthpotion","healthpotion","healthpotion"]
    loot = random.randint(0,len(typesofloot) - 1)
    loot = str(typesofloot [loot])
    loot_text = ''
    if loot == 'healthpotion':
        addhealthpotion(bot, instigator)
        loot_text = ': worth 100 health. Use .challengehealthpotion to consume.'
    return loot, loot_text

def lootcorpse(bot, loser, winner):
    loserhealthpotions = get_healthpotions(bot, loser)
    if loserhealthpotions:
        bot.db.set_nick_value(loser, 'challenges_healthpotions', '')
        winnerhealthpotions = get_healthpotions(bot, winner)
        bot.db.set_nick_value(winner, 'challenges_healthpotions', int(winnerhealthpotions) + int(loserhealthpotions))

####################
## Health Potions ##
####################

def get_healthpotions(bot, nick):
    healthpotions = bot.db.get_nick_value(nick, 'challenges_healthpotions') or 0
    return healthpotions

def addhealthpotion(bot, nick):
    healthpotions = get_healthpotions(bot, nick)
    bot.db.set_nick_value(nick, 'challenges_healthpotions', int(healthpotions) + 1)

@module.require_chanmsg
@module.commands('challengehealthpotion')
def usehealthpotion(bot, trigger):
    instigator = trigger.nick
    target = trigger.nick
    targetdisenable = get_spicebotdisenable(bot, target)
    if targetdisenable:
        channel = trigger.sender
        target = trigger.group(3) or trigger.nick
        healthpotions = get_healthpotions(bot, trigger.nick)
        if healthpotions:
            health = get_health(bot, target)
            if target == trigger.nick:
                bot.say(trigger.nick + ' uses health potion.')
            elif target.lower() not in bot.privileges[channel.lower()]:
                bot.say("I'm not sure who that is.")
            else:
                bot.say(trigger.nick + ' uses health potion on ' + target + ".")
            bot.db.set_nick_value(target, 'challenges_health', int(health) + 100)
            bot.db.set_nick_value(trigger.nick, 'challenges_healthpotions', int(healthpotions) - 1)
        else:
            bot.say('You do not have a healthpotion to use!')
    else:
        instigator = trigger.nick
        warned = bot.db.get_nick_value(target, 'spicebothour_warn') or 0
        if not warned:
            bot.notice(target + ", you have to run .spiceboton to allow her to listen to you.", instigator)
        else:
            bot.notice(target + ", it looks like your access to spicebot has been disabled for a while. Check out ##SpiceBotTest.", instigator)
        
######################
## Weapon Selection ##
######################

def weaponofchoice(bot):
    weaponslist = get_weaponslocker(bot)
    weapon =random.choice(weaponslist)
    if not weapon:
        weapon = "fist"
    if weapon.startswith('a') or weapon.startswith('e') or weapon.startswith('i') or weapon.startswith('o') or weapon.startswith('u'):
        weapon = str('an ' + weapon)
    else:
        weapon = str('a ' + weapon)
    return weapon

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
    return damage

###################
## Select Winner ##
###################

def getwinner(bot, instigator, target):
    instigatorxp = get_xp(bot, instigator)
    if not instigatorxp:
        instigatorxp = '1'
    targetxp = get_xp(bot, target)
    if not targetxp:
        targetxp = '1'
    
    ## each person
    instigatorfight = '1'
    targetfight = '1'
    
    # instigator gets 1 for surprise
    instigatorfight = int(instigatorfight) + 1
    
    # XP difference
    if int(instigatorxp) > int(targetxp):
        instigatorfight = int(instigatorfight) + 1
    elif int(instigatorxp) < int(targetxp):
        targetfight = int(targetfight) + 1
    elif int(instigatorxp) == int(targetxp):
        instigatorfight = int(instigatorfight) + 1
        targetfight = int(targetfight) + 1
    else:
        instigatorfight = int(instigatorfight) + 1
        targetfight = int(targetfight) + 1
    
    ## Random Number
    flip = randint(0, 1)
    if (flip == 0):
        instigatorfight = int(instigatorfight) + 1
    else:
        targetfight = int(targetfight) + 1

    ## Dice Roll
    instigatorfightarray = []
    targetfightarray = []
    while int(instigatorfight) != 0:
        instigatorfightroll = diceroll()
        instigatorfightarray.append(instigatorfightroll)
        instigatorfight = int(instigatorfight) - 1
    instigatorfight = max(instigatorfightarray)
    while int(targetfight) != 0:
        targetfightroll = diceroll()
        targetfightarray.append(targetfightroll)
        targetfight = int(targetfight) - 1
    targetfight = max(targetfightarray)
            
    ## tie breaker
    if instigatorfight == targetfight:
        tiebreaker = randint(0, 1)
        if (tiebreaker == 0):
            instigatorfight = int(instigatorfight) + 1
        else:
            targetfight = int(targetfight) + 1

    ## Compare
    if int(instigatorfight) > int(targetfight):
        winner = instigator
    else:
        winner = target
    ## LOSER IS NOT WINNER
    if winner == instigator:
        loser = target
    else:
        loser = instigator
    return winner, loser

###############
## ScoreCard ##
###############

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

###############
## XP points ##
###############

def get_xp(bot, nick):
    xp = bot.db.get_nick_value(nick, 'challenges_xp') or 0
    return xp

def update_xp(bot, nick, damage):
    xp = get_xp(bot, nick)
    bot.db.set_nick_value(nick, 'challenges_xp', xp + int(damage))
    currentxp = get_xp(bot, nick)
    return currentxp

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

####################
## Weapons Locker ##
####################

@module.require_admin
@sopel.module.commands('weaponslockeraddold')
def weaponslockercmdold(bot, trigger):
    with open (weaponslocker, "r") as myfile:
        bot.say('adding existing weapons')
        for line in myfile:
            weaponslist = get_weaponslocker(bot)
            weaponchange = str(line)
            if weaponchange not in weaponslist:
                weaponslist.append(weaponchange)
                update_weaponslocker(bot, weaponslist)
                weaponslist = get_weaponslocker(bot)
        bot.say('old weapons added')
    
@sopel.module.commands('weaponslocker','weaponslockeradd','weaponslockerdel','weaponslockerinv')
def weaponslockercmd(bot, trigger):
    instigator = trigger.nick
    target = trigger.nick
    targetdisenable = get_spicebotdisenable(bot, target)
    if targetdisenable:
        commandtrimmed = trigger.group(1)
        commandtrimmed = str(commandtrimmed.split("weaponslocker", 1)[1])
        weaponslist = get_weaponslocker(bot)
        if commandtrimmed == '':
            bot.say('Use weaponslockeradd or weaponslockerdel to adjust Locker Inventory.')
        elif commandtrimmed == 'inv' and trigger.admin:
            ## cleanup
            weaponslistnew = []
            for weapon in weaponslist:
                if weapon.endswith("\n"):
                    weaponslist.remove(weapon)
                    weapon = weapon.replace("\n", '')
                    weaponslistnew.append(weapon)
                else:
                    weaponslist.remove(weapon)
                    weaponslistnew.append(weapon)
            for weapon in weaponslistnew:
                if weapon not in weaponslist:
                    weaponslist.append(weapon)
            update_weaponslocker(bot, weaponslist)
            weaponslist = get_weaponslocker(bot)
            weaponslist = str(weaponslist)
            weaponslist = weaponslist.replace('[', '')
            weaponslist = weaponslist.replace(']', '')
            weaponslist = weaponslist.replace("u'", '')
            weaponslist = weaponslist.replace("'", '')
            bot.say(str(weaponslist))
        #elif commandtrimmed == 'inv' and trigger.admin:
            #bot.say('test')
            #weaponslistnew = []
            #for weapon in weaponslist:
                #if weapon.endswith("\n"):
                    #bot.say(str(weapon)
                #else:
                    bot.say(str(weapon)
                    #weapon = str(weapon.split("\n", 0)[1])
                #weaponslistnew.append(weapon)
            #for channel in bot.channels:
                #bot.db.set_nick_value(channel, 'weapons_locker', '')
            #for weapon in weaponslistnew:
                #weaponslist = get_weaponslocker(bot)
                #if weapon not in weaponslist:
                    #weaponslist.append(weapon)
            #weaponslist = get_weaponslocker(bot)
            #weaponslist = str(weaponslist)
            #weaponslist = weaponslist.replace('[', '')
            #weaponslist = weaponslist.replace(']', '')
            #weaponslist = weaponslist.replace("u'", '')
            #weaponslist = weaponslist.replace("'", '')
            #bot.say(str(weaponslist))
        elif not trigger.group(2):
            bot.say("What weapon would you like to add/remove?")
        else:
            weaponchange = str(trigger.group(2))
            if commandtrimmed == 'add':
                if weaponchange in weaponslist:
                    bot.say(weaponchange + " is already in the weapons locker.")
                    rescan = 'False'
                else:
                    weaponslist.append(weaponchange)
                    update_weaponslocker(bot, weaponslist)
                    rescan = 'True'
            elif commandtrimmed == 'del':
                if weaponchange not in weaponslist:
                    bot.say(weaponchange + " is not in the weapons locker.")
                    rescan = 'False'
                else:
                    weaponslist.remove(weaponchange)
                    update_weaponslocker(bot, weaponslist)
                    rescan = 'True'
            if rescan == 'True':
                weaponslist = get_weaponslocker(bot)
                if weaponchange in weaponslist:
                    bot.say(weaponchange + " has been added to the weapons locker.")
                else:
                    bot.say(weaponchange + ' has been removed from the weapons locker.')
    else:
        instigator = trigger.nick
        warned = bot.db.get_nick_value(target, 'spicebothour_warn') or 0
        if not warned:
            bot.notice(target + ", you have to run .spiceboton to allow her to listen to you.", instigator)
        else:
            bot.notice(target + ", it looks like your access to spicebot has been disabled for a while. Check out ##SpiceBotTest.", instigator)

def get_weaponslocker(bot):
    for channel in bot.channels:
        weaponslist = bot.db.get_nick_value(channel, 'weapons_locker') or []
        return weaponslist

def update_weaponslocker(bot, weaponslist):
    for channel in bot.channels:
        bot.db.set_nick_value(channel, 'weapons_locker', weaponslist)
        
###########
## Stats ##
###########

@module.require_chanmsg
@module.commands('challenges','duels')
def challengesa(bot, trigger):
    instigator = trigger.nick
    target = trigger.nick
    targetdisenable = get_spicebotdisenable(bot, target)
    if targetdisenable:
        channel = trigger.sender
        target = trigger.group(3) or trigger.nick
        if target.lower() not in bot.privileges[channel.lower()]:
            bot.say("I'm not sure who that is.")
        else:
            stats = ''
            challengestatsarray = ['health','xp','wins','losses','respawns','timeout','healthpotions']
            for x in challengestatsarray:
                scriptdef = str('get_' + x + '(bot,target)')
                databasecolumn = str('challenges_' + x)
                gethowmany = eval(scriptdef)
                if gethowmany:
                    addstat = str(' ' + str(x) + "=" + str(gethowmany))
                    stats = str(stats + addstat)
            if stats != '':
                stats = str(target + "'s stats:" + stats)
                bot.say(stats)
            else:
                bot.say('No stats found for ' + target)
    else:
        instigator = trigger.nick
        warned = bot.db.get_nick_value(target, 'spicebothour_warn') or 0
        if not warned:
            bot.notice(target + ", you have to run .spiceboton to allow her to listen to you.", instigator)
        else:
            bot.notice(target + ", it looks like your access to spicebot has been disabled for a while. Check out ##SpiceBotTest.", instigator)
        
###########
## Tools ##
###########

def diceroll():
    diceroll = randint(0, 6)
    return diceroll

#################
## Stats Clear ##
#################

@sopel.module.require_admin
@module.require_chanmsg
@module.commands('challengestatsadminall','challengestatsadmin','challengestatsadminwins','challengestatsadminlosses','challengestatsadminhealth','challengestatsadminhealthpotions','challengestatsadminrespawns','challengestatsadminxp','challengestatsadmintime','challengestatsadmindisenable')
def challengestatsadmin(bot, trigger):
    channel = trigger.sender
    commandtrimmed = trigger.group(1)
    commandtrimmed = str(commandtrimmed.split("challengestatsadmin", 1)[1])
    if commandtrimmed == '':
         bot.say('Repeat this command with: wins,losses,health,healthpotions,respawns,xp,time,disenable')
    elif commandtrimmed == 'all':
        challengestatsarray = ['wins','losses','health','healthpotions','respawns','xp','timeout','disenable']
        if not trigger.group(3):
            target = trigger.nick
            bot.say('Resetting all stats for ' + target + '.')
            for x in challengestatsarray:
                scriptdef = str('get_' + x)
                databasecolumn = str('challenges_' + x)
                gethowmany = eval(scriptdef)
                if gethowmany:
                    bot.db.set_nick_value(target, databasecolumn, '')
        elif trigger.group(3) == 'all':
            bot.say('Resetting all stats for Channel.')
            for u in bot.channels[channel].users:
                target = u
                for x in challengestatsarray:
                    scriptdef = str('get_' + x)
                    databasecolumn = str('challenges_' + x)
                    gethowmany = eval(scriptdef)
                    if gethowmany:
                        bot.db.set_nick_value(target, databasecolumn, '')
            bot.say('Resetting of all stats for all in channel is complete.')
        else:
            target = trigger.group(3)
            bot.say('Resetting all stats for ' + target + '.')
            for x in challengestatsarray:
                scriptdef = str('get_' + x)
                databasecolumn = str('challenges_' + x)
                gethowmany = eval(scriptdef)
                if gethowmany:
                    bot.db.set_nick_value(target, databasecolumn, '')
    else:
        scriptdef = str('get_' + commandtrimmed)
        databasecolumn = str('challenges_' + commandtrimmed)
        if not trigger.group(3):
            target = trigger.nick
            bot.say('Resetting ' + str(commandtrimmed) + ' stat for ' + target + '.')
            gethowmany = eval(scriptdef)
            if gethowmany:
                bot.db.set_nick_value(target, databasecolumn, '')
        elif trigger.group(3) == 'all':
            bot.say('Resetting ' + str(commandtrimmed) + ' stat for all in channel.')
            for u in bot.channels[channel].users:
                target = u
                gethowmany = eval(scriptdef)
                if gethowmany:
                    bot.db.set_nick_value(target, databasecolumn, '')
            bot.say('Resetting of ' + str(commandtrimmed) + ' stat for all in channel is complete.')
        else:
            target = trigger.group(3)
            bot.say('Resetting ' + str(commandtrimmed) + ' stat for ' + target)
            gethowmany = eval(scriptdef)
            if gethowmany:
                bot.db.set_nick_value(target, databasecolumn, '')

                
def update_usertotal(bot, nick):
    usertotal = bot.db.get_nick_value(nick, 'spicebot_usertotal') or 0
    bot.db.set_nick_value(nick, 'spicebot_usertotal', usertotal + 1)
