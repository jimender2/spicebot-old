import sopel.module
import sopel
from sopel import module, tools
import random
from random import randint
import time
import re
import sys
import os
from os.path import exists
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

TIMEOUT = 180
TIMEOUTC = 40
ALLCHAN = 'entirechannel'
OPTTIMEOUT = 3600

## React to /me (ACTION) challenges
@module.rule('^(?:challenges|(?:fi(?:ght|te)|duel)s(?:\s+with)?)\s+([a-zA-Z0-9\[\]\\`_\^\{\|\}-]{1,32}).*')
@module.intent('ACTION')
@module.require_chanmsg
def challenge_action(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        inchannel = trigger.sender
        target = trigger.group(3)
        if not inchannel.startswith("#"):
            bot.say('Duels must be in channel')
        else:
            return challenge(bot, trigger.sender, trigger.nick, trigger.group(3))
        
####################
## Main Operation ##
####################

@sopel.module.commands('challenge','duel')
def challenge_cmd(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        return mainfunction(bot, trigger)
        
def mainfunction(bot, trigger):
    options = str("on/off, stats, poisonpotion, healthpotion, weaponslocker")
    instigator = trigger.nick
    inchannel = trigger.sender
    for c in bot.channels:
        channel = c
    if not trigger.group(2):
        bot.notice(instigator + ", Who did you want to challenge? Other Options are: " + str(options), instigator)
    else:
        fullcommandused = trigger.group(2)
        commandused = trigger.group(3)
        target = trigger.group(4)
        if not target:
            target = trigger.nick

        ## On/off
        if commandused == 'on' or commandused == 'off':
            if target == 'all':
                if trigger.admin:
                    bot.say("Turning Challenges " +  commandused + ' for all.')
                    for u in bot.channels[channel].users:
                        target = u
                        disenable = get_disenable(bot, target)
                        if commandused == 'on':
                            bot.db.set_nick_value(target, 'challenges_disenable', 'true')
                        else:
                            bot.db.set_nick_value(target, 'challenges_disenable', '')
                    bot.say('Challenges turned ' + commandused + ' for all.')
                else:
                    bot.say('Only Admin can Change Statuses for all.')
            elif target.lower() not in bot.privileges[channel.lower()]:
                bot.say("I'm not sure who that is.")
            else:
                disenable = get_disenable(bot, target)
                opttime = get_opttimeout(bot, target)
                if opttime < OPTTIMEOUT and not bot.nick.endswith('dev') and not trigger.admin:
                    bot.notice(target + " can't enable/disable challenges for %d seconds." % (OPTTIMEOUT - opttime), instigator)
                if not disenable:
                    if commandused == 'on':
                        bot.db.set_nick_value(target, 'challenges_disenable', 'true')
                        adjustment = 'now'
                        set_opttimeout(bot, target)
                    else:
                        adjustment = 'already'
                else:
                    if commandused == 'on':
                        adjustment = 'already'
                    else:
                        bot.db.set_nick_value(target, 'challenges_disenable', '')
                        adjustment = 'now'
                        set_opttimeout(bot, target)
                message = str('Challenges is ' + adjustment + ' ' + commandused + ' for '  + target)
                bot.say(message)
        
        ## Stats
        elif commandused == 'stats':
            disenable = get_disenable(bot, target)
            if not disenable:
                bot.say(target + " does not have Challenges enabled")
            elif target.lower() not in bot.privileges[channel.lower()]:
                bot.say("I'm not sure who that is.")
            else:
                stats = ''
                challengestatsarray = ['health','xp','wins','losses','winlossratio','respawns','healthpotions','poisonpotions','timeout']
                for x in challengestatsarray:
                    scriptdef = str('get_' + x + '(bot,target)')
                    gethowmany = eval(scriptdef)
                    if gethowmany:
                        addstat = str(' ' + str(x) + "=" + str(gethowmany))
                        stats = str(stats + addstat)
                if stats != '':
                    stats = str(target + "'s stats:" + stats)
                    bot.say(stats)
                else:
                    bot.say('No stats found for ' + target)
        
        ## Enable/Disable status
        elif commandused == 'status' and not inchannel.startswith("#"):
            disenable = get_disenable(bot, target)
            if disenable:
                message = str(target + " has Challenges enabled")
            else:
                message = str(target + " does not have Challenges enabled")
            bot.notice(message, instigator)
            
        ## Weaponslocker
        elif commandused == 'weaponslocker':
            weaponslist = get_weaponslocker(bot, instigator)
            adjustmentdirection = trigger.group(4)
            if not adjustmentdirection:
                bot.say('Use .duel weaponslocker add/del to adjust Locker Inventory.')
            elif adjustmentdirection == 'inv' and not inchannel.startswith("#"):
                weaponslistnew = []
                for weapon in weaponslist:
                    weapon = str(weapon)
                    weaponslistnew.append(weapon)
                for channel in bot.channels:
                    bot.db.set_nick_value(channel, 'weapons_locker', '')
                for weapon in weaponslistnew:
                    if weapon not in weaponslist:
                        weaponslist.append(weapon)
                update_weaponslocker(bot, instigator, weaponslist)
                weaponslist = get_weaponslocker(bot, instigator)
                weaponslist = str(weaponslist)
                weaponslist = weaponslist.replace('[', '')
                weaponslist = weaponslist.replace(']', '')
                weaponslist = weaponslist.replace("u'", '')
                weaponslist = weaponslist.replace('u"', '')
                weaponslist = weaponslist.replace("'", '')
                weaponslist = weaponslist.replace('"', '')
                bot.say(str(weaponslist))
            elif adjustmentdirection == 'inv' and inchannel.startswith("#"):
                bot.say('Inventory can only be viewed in privmsg.')
            else:
                weaponchange = str(fullcommandused.split(adjustmentdirection, 1)[1]).strip()
                if not weaponchange:
                    bot.say("What weapon would you like to add/remove?")
                else:
                    if weaponchange in weaponslist:
                        if adjustmentdirection == 'add':
                            weaponlockerstatus = 'already'
                        else:
                            weaponslist.remove(weaponchange)
                            update_weaponslocker(bot, instigator, weaponslist)
                            weaponlockerstatus = 'no longer'
                    else:
                        if adjustmentdirection == 'add':
                            weaponslist.append(weaponchange)
                            update_weaponslocker(bot, instigator, weaponslist)
                            weaponlockerstatus = 'now'
                        else:
                            weaponlockerstatus = 'already not'
                    message = str(weaponchange + " is " + weaponlockerstatus + " in your weapons locker.")
                    bot.say(message)
                
        ## Leaderboard
        elif commandused == 'leader':
            currentleader = ''
            currentleadernumber = 0
            for u in bot.channels[channel].users:
                target = u
                disenable = get_disenable(bot, target)
                if disenable:
                    winlossratio = get_winlossratio(bot,target)
                    if winlossratio > currentleadernumber:
                        currentleader = target
                        currentleadernumber = winlossratio
            leaderboardscript = str("The Current Leader in the room is: " + str(currentleader) + " with a ratio of: " + str(currentleadernumber))
            bot.say(leaderboardscript)
            
        ## healthpotion
        elif commandused == 'healthpotion':
            usepotion = 0
            healthpotions = get_healthpotions(bot, instigator)
            if healthpotions:
                health = get_health(bot, target)
                if target == trigger.nick:
                    bot.say(trigger.nick + ' uses health potion.')
                    usepotion = 1
                elif target.lower() not in bot.privileges[channel.lower()]:
                    bot.say("I'm not sure who that is.")
                else:
                    targetdisenable = get_disenable(bot, target)
                    if targetdisenable:
                        bot.say(trigger.nick + ' uses health potion on ' + target + ".")
                        usepotion = 1
                if usepotion == 1:
                    if not inchannel.startswith("#") and not trigger.nick:
                        bot.notice(instigator + " used a healthpotion on you", target)
                    bot.db.set_nick_value(target, 'challenges_health', int(health) + 100)
                    bot.db.set_nick_value(trigger.nick, 'challenges_healthpotions', int(healthpotions) - 1)
            else:
                bot.say('You do not have a healthpotion to use!')
                
        ## poisonpotion
        elif commandused == 'poisonpotion':
            usepotion = 0
            poisonpotions = get_poisonpotions(bot, instigator)
            if poisonpotions:
                health = get_health(bot, target)
                if target == trigger.nick:
                    bot.say(trigger.nick + ' uses poisonpotion.')
                    usepotion = 1
                elif target.lower() not in bot.privileges[channel.lower()]:
                    bot.say("I'm not sure who that is.")
                else:
                    targetdisenable = get_disenable(bot, target)
                    if targetdisenable:
                        bot.say(trigger.nick + ' uses poisonpotion on ' + target + ".")
                        usepotion = 1
                if usepotion == 1:
                    if not inchannel.startswith("#") and not trigger.nick:
                        bot.notice(instigator + " used a poisonpotion on you", target)
                    bot.db.set_nick_value(target, 'challenges_health', int(health) - 50)
                    bot.db.set_nick_value(trigger.nick, 'challenges_poisonpotions', int(poisonpotions) - 1)
            else:
                bot.say('You do not have a poisonpotion to use!')
                
        ## Combat
        else:
            target = trigger.group(3)
            if not inchannel.startswith("#"):
                bot.say('Duels must be in channel')
            elif not target:
                bot.notice(instigator + ", Who did you want to fight?", instigator)
            elif target == bot.nick:
                bot.say("I refuse to fight a biological entity!")
            elif target == instigator:
                bot.say("If you are feeling self-destructive, there are places you can call.")
            elif target.lower() not in bot.privileges[channel.lower()]:
                bot.say("I'm not sure who that is.")
            else:
                return challenge(bot, channel, instigator, target)

## Health Regeneration
@sopel.module.interval(1800)
def healthregen(bot):
    for channel in bot.channels:
        for u in bot.privileges[channel.lower()]:
            target = u
            targetdisenable = get_disenable(bot, target)
            if targetdisenable:
                health = get_health(bot, target)
                if health < 500:
                    bot.db.set_nick_value(target, 'challenges_health', int(health) + 50)
                    health = get_health(bot, target)
     
####################
## Main Operation ##
####################

def challenge(bot, channel, instigator, target):
    
    ## Don't allow chat spamming
    instigatortime = get_timesince(bot, instigator)
    targettime = get_timesince(bot, target)
    channeltime = get_timesince(bot, ALLCHAN)
        
    ## Bot opt-out
    targetspicebotdisenable = get_spicebotdisenable(bot, target)
        
    ## People can opt out of playing
    instigatordisenable = get_disenable(bot, instigator)
    targetdisenable = get_disenable(bot, target)
        
    ## Check Opt-in Status
    if not targetspicebotdisenable:
        bot.notice(instigator + ', It looks like ' + target + ' has disabled Spicebot.', instigator)
    elif not instigatordisenable:
        bot.notice(instigator + ", It looks like you have disabled Challenges. Run .challenge on to re-enable.", instigator)
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
        announcecombatmsg = str(instigator + " versus " + target)
        
        ## Check new player health, initial Spawn
        update_spawn(bot, instigator)
        update_spawn(bot, target)

        ## Damage Done
        damage = damagedone(bot)

        ## Select Winner
        winner, loser = getwinner(bot, instigator, target)

        ## Weapon Select
        weapon = weaponofchoice(bot, winner)
           
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
            winnermsg = str(winner + ' killed ' + loser + " with " + weapon + ' forcing a respawn!!')
            update_respawn(bot, loser)
            ## Loot Corpse
            lootcorpse(bot, loser, winner)
        else:
            winnermsg = str(winner + " hits " + loser + " with " + weapon + ', dealing ' + damage + ' damage.')
            
        ## Random Inventory gain
        randominventoryfind = randominventory()
        if randominventoryfind == 'true':
            if winner == instigator:
                loot, loot_text = determineloottype(bot, winner)
                lootwinnermsgb = ''
            else:
                loot, loot_text = determineloottype(bot, winner)
                lootwinnermsgb = str(winner + " gains the " + str(loot))
                lootwinnermsg = str(instigator + ' found a ' + str(loot) + ' ' + str(loot_text))
        else:
            lootwinnermsg = ''
            lootwinnermsgb = ''
            
        ## On Screen Text
        bot.say(str(announcecombatmsg) + "       " + str(lootwinnermsg))
        bot.say(str(winnermsg)+ "       " + str(lootwinnermsgb))
            
        ## Update Time Of Combat
        update_time(bot, instigator)
        update_time(bot, target)
        update_time(bot, ALLCHAN)
            
#################
## Stats Clear ##
#################

@sopel.module.require_admin
@module.commands('challengestatsadminall','challengestatsadmin','challengestatsadminwins','challengestatsadminlosses','challengestatsadminhealth','challengestatsadminhealthpotions','challengestatsadminrespawns','challengestatsadminxp','challengestatsadmintime','challengestatsadmindisenable','challengestatsadminpoisonpotions')
def challengestatsadmin(bot, trigger):
    for c in bot.channels:
            channel = c
    commandtrimmed = trigger.group(1)
    commandtrimmed = str(commandtrimmed.split("challengestatsadmin", 1)[1])
    if commandtrimmed == '':
         bot.say('Repeat this command with: wins,losses,health,healthpotions,respawns,xp,time,disenable,poisonpotions')
    elif commandtrimmed == 'all':
        challengestatsarray = ['wins','losses','health','healthpotions','respawns','xp','timeout','disenable','poisonpotions']
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
        
## Functions######################################################################################################################

#############
## Opt Out ##
#############

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
    
def reset_opttimeout(bot, nick):
    bot.db.set_nick_value(nick, 'challengesopt_time', '')
    
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

def determineloottype(bot, nick):
    typesofloot  = ["healthpotion","poisonpotion","healthpotion","poisonpotion","healthpotion","poisonpotion","healthpotion"]
    loot = random.randint(0,len(typesofloot) - 1)
    loot = str(typesofloot [loot])
    loot_text = ''
    if loot == 'healthpotion':
        addhealthpotion(bot, nick)
        loot_text = ': worth 100 health. Use .challenge healthpotion to consume.'
    if loot == 'poisonpotion':
        addpoisonpotion(bot, nick)
        loot_text = ': worth -50 health. Use .challenge poisonpotion to consume.'
    return loot, loot_text

def lootcorpse(bot, loser, winner):
    loserhealthpotions = get_healthpotions(bot, loser)
    loserpoisonpotions = get_poisonpotions(bot, loser)
    if loserhealthpotions:
        bot.db.set_nick_value(loser, 'challenges_healthpotions', '')
        winnerhealthpotions = get_healthpotions(bot, winner)
        bot.db.set_nick_value(winner, 'challenges_healthpotions', int(winnerhealthpotions) + int(loserhealthpotions))
    if loserpoisonpotions:
        bot.db.set_nick_value(loser, 'challenges_poisonpotions', '')
        winnerpoisonpotions = get_poisonpotions(bot, winner)
        bot.db.set_nick_value(winner, 'challenges_poisonpotions', int(winnerpoisonpotions) + int(loserpoisonpotions))
        
####################
## Health Potions ##
####################

def get_healthpotions(bot, nick):
    healthpotions = bot.db.get_nick_value(nick, 'challenges_healthpotions') or 0
    return healthpotions

def addhealthpotion(bot, nick):
    healthpotions = get_healthpotions(bot, nick)
    bot.db.set_nick_value(nick, 'challenges_healthpotions', int(healthpotions) + 1)

####################
## poison Potions ##
####################

def get_poisonpotions(bot, nick):
    posionpotions = bot.db.get_nick_value(nick, 'challenges_poisonpotions') or 0
    return posionpotions

def addpoisonpotion(bot, nick):
    poisonpotions = get_poisonpotions(bot, nick)
    bot.db.set_nick_value(nick, 'challenges_poisonpotions', int(poisonpotions) + 1)
    
######################
## Weapon Selection ##
######################

def weaponofchoice(bot, nick):
    weaponslist = get_weaponslocker(bot, nick)
    try:
        weapon =random.choice(weaponslist)
    except IndexError:
        weapon = "fist"
    weapon = str(weapon)
    if weapon.startswith('a ') or weapon.startswith('an ') or weapon.startswith('the '):
        weapon = str(weapon)
    elif weapon.startswith('a') or weapon.startswith('e') or weapon.startswith('i') or weapon.startswith('o') or weapon.startswith('u'):
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

def get_winlossratio(bot,target):
    wins = get_wins(bot, target)
    losses = get_losses(bot, target)
    winlosstotal = abs(wins + losses)
    winlossratio = float(wins)/winlosstotal
    return winlossratio
###############
## XP points ##
###############

def get_xp(bot, nick):
    xp = bot.db.get_nick_value(nick, 'challenges_xp') or 0
    return xp

def update_xp(bot, nick, XPearned):
    xp = get_xp(bot, nick)
    bot.db.set_nick_value(nick, 'challenges_xp', xp + int(XPearned))
    currentxp = get_xp(bot, nick)
    return currentxp

############
## Health ##
############

def get_health(bot, nick):
    health = bot.db.get_nick_value(nick, 'challenges_health') or 1000
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

def get_weaponslocker(bot, nick):
    for channel in bot.channels:
        weaponslist = bot.db.get_nick_value(nick, 'weapons_locker') or []
        return weaponslist

def update_weaponslocker(bot, nick, weaponslist):
    for channel in bot.channels:
        bot.db.set_nick_value(nick, 'weapons_locker', weaponslist)
        
###########
## Tools ##
###########

def diceroll():
    diceroll = randint(0, 6)
    return diceroll
