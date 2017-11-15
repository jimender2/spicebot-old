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

## Configurables #############
TIMEOUT = 180
TIMEOUTC = 40
ALLCHAN = 'entirechannel'
OPTTIMEOUT = 1800
lootitemsarray = ['healthpotion','manapotion','poisonpotion','timepotion','mysterypotion']
challengestatsadminarray = ['wins','losses','health','mana','healthpotion','mysterypotion','timepotion','respawns','xp','kills','timeout','disenable','poisonpotion','manapotion','lastfought','konami']
challengestatsarray = ['health','mana','xp','wins','losses','winlossratio','respawns','kills','backpackitems','lastfought','timeout']

####################
## Main Operation ##
####################

@sopel.module.commands('challenge','duel')
def challenge_cmd(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        return mainfunction(bot, trigger)
        
def mainfunction(bot, trigger):
    instigator = trigger.nick
    inchannel = trigger.sender
    for c in bot.channels:
        channel = c
    if not trigger.group(2):
        bot.notice(instigator + ", Who did you want to challenge? Online Docs: https://github.com/deathbybandaid/sopel-modules/blob/master/otherfiles/ChallengesDocumentation.md", instigator)
    else:
        fullcommandused = trigger.group(2)
        commandused = trigger.group(3)
        target = trigger.group(4)
        if not target:
            target = trigger.nick
            
        ## Docs
        elif commandused == 'docs' or commandused == 'help':
            bot.say("Online Docs: https://github.com/deathbybandaid/sopel-modules/blob/master/otherfiles/ChallengesDocumentation.md")
            
        ## On/off
        if commandused == 'on' or commandused == 'off':
            bot.say("Attempting to turn challenges " +  commandused + ' for ' + target + '.')
            if target == 'all' and trigger.admin:
                for u in bot.channels[channel].users:
                    target = u
                    disenable = get_disenable(bot, target)
                    if commandused == 'on':
                        bot.db.set_nick_value(target, 'challenges_disenable', 'true')
                    else:
                        bot.db.set_nick_value(target, 'challenges_disenable', '')
            elif target == 'all' and not trigger.admin:
                bot.say('Only Admin can Change Statuses for all.')
            elif target.lower() not in bot.privileges[channel.lower()]:
                bot.say("I'm not sure who that is.")
            else:
                disenable = get_disenable(bot, target)
                opttime = get_opttimeout(bot, target)
                if opttime < OPTTIMEOUT and not bot.nick.endswith('dev') and not trigger.admin:
                    bot.notice(target + " can't enable/disable challenges for %d seconds." % (OPTTIMEOUT - opttime), instigator)
                elif not disenable:
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
            bot.say("Challenges should now be " +  commandused + ' for ' + target + '.')
        
        ## Stats
        elif commandused == 'stats':
            disenable = get_disenable(bot, target)
            if not disenable and target != instigator:
                bot.say(target + " does not have Challenges enabled")
            elif target.lower() not in bot.privileges[channel.lower()]:
                bot.say("I'm not sure who that is.")
            else:
                stats = ''
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
        
        ## backpack
        elif commandused == 'backpack':
            disenable = get_disenable(bot, target)
            if not disenable:
                bot.say(target + " does not have Challenges enabled")
            elif target.lower() not in bot.privileges[channel.lower()]:
                bot.say("I'm not sure who that is.")
            else:
                stats = ''
                for x in lootitemsarray:
                    gethowmany = get_lootitem(bot, target, x)
                    if gethowmany:
                        addstat = str(' ' + str(x) + "=" + str(gethowmany))
                        stats = str(stats + addstat)
                if stats != '':
                    stats = str(target + "'s backpack:" + stats)
                    bot.say(stats)
                else:
                    bot.say('No backpack items found for ' + target)
                    
        ## Stats statsadmin
        elif commandused == 'statsadmin' and trigger.admin:
            target = trigger.group(4)
            statsadminarray = ['set','reset']
            commandtrimmed = trigger.group(5)
            statset = trigger.group(6)
            newvalue = str(fullcommandused.split(statset, 1)[1]).strip()
            if target.lower() not in bot.privileges[channel.lower()] and target != 'everyone':
                bot.say("I'm not sure who that is.")
            elif commandtrimmed not in statsadminarray:
                bot.say("A correct command use is .duel statsadmin target set/reset stat")
            elif statset not in challengestatsadminarray and statset != 'all':
                bot.say("A correct command use is .duel statsadmin target set/reset stat")
            elif commandtrimmed == 'set' and not newvalue:
                bot.say("A correct command use is .duel statsadmin target set stat value")
            else:
                if not newvalue:
                    newvalue = ''
                if target == 'everyone':
                    for u in bot.channels[channel].users:
                        etarget = u
                        if statset == 'all':
                            for x in challengestatsadminarray:
                                estatset = x
                                databasecolumn = str('challenges_' + estatset)
                                bot.db.set_nick_value(etarget, databasecolumn, newvalue)
                        else:
                            databasecolumn = str('challenges_' + statset)
                            bot.db.set_nick_value(target, databasecolumn, newvalue)
                else:
                    if statset == 'all':
                        for x in challengestatsadminarray:
                            statset = x
                            databasecolumn = str('challenges_' + statset)
                            bot.db.set_nick_value(target, databasecolumn, newvalue)
                    else:
                        databasecolumn = str('challenges_' + statset)
                        bot.db.set_nick_value(target, databasecolumn, newvalue)
                bot.say('Possibly done.')
            
        ## Enable/Disable status
        elif commandused == 'status':
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
                chunks = weaponslist.split()
                per_line = 15
                for i in range(0, len(chunks), per_line):
                    weaponline = " ".join(chunks[i:i + per_line])
                    bot.say(str(weaponline))
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
        
        ## Konami
        elif commandused == 'upupdowndownleftrightleftrightba':
            konami = get_konami(bot, instigator)
            if not konami:
                set_konami(bot, instigator)
                bot.notice(instigator + " you have found the cheatcode easter egg!!!", instigator)
            else:
                bot.notice(instigator + " you can only cheat once.", instigator)
        
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
            
        ## Close to death
        elif commandused == 'closetodeath':
            currentleader = ''
            currentleadernumber = 9999999999
            for u in bot.channels[channel].users:
                target = u
                disenable = get_disenable(bot, target)
                if disenable:
                    health = get_health(bot,target)
                    if health < currentleadernumber:
                        currentleader = target
                        currentleadernumber = health
            leaderboardscript = str("The Current person close to death in the room is: " + str(currentleader) + " with health at: " + str(currentleadernumber))
            bot.say(leaderboardscript)
        
        ## Magic Attack
        elif commandused == 'magic':
            magicoptions = ['attack','instakill','health']
            magicusage = trigger.group(4)
            if magicusage not in magicoptions:
                bot.say('Magic uses include: attack, instakill, health')
            else:
                target = trigger.group(5)
                if not target:
                    target = trigger.nick
                mana = get_mana(bot, instigator)
                if magicusage == 'attack':
                    manarequired = 250
                    damage = 200
                elif magicusage == 'health':
                    manarequired = 200
                    damage = -200
                elif magicusage == 'instakill':
                    manarequired = 1000
                    damage = 99999
                if not mana:
                    bot.notice(instigator + " you don't have any mana.", instigator)
                elif mana < manarequired:
                    manamath = int(manarequired - mana)
                    bot.notice(instigator + " you need " + str(manamath) + " more mana to do this attack.", instigator)
                else:
                    if target.lower() not in bot.privileges[channel.lower()]:
                        bot.say("I'm not sure who that is.")
                    else:
                        targethealthstart = get_health(bot, target)
                        use_magicattack(bot, instigator, target, damage)
                        targethealth = get_health(bot, target)
                        if targethealth <= 0:
                            update_respawn(bot, target)
                            respawn_mana(bot, target)
                            update_kills(bot, instigator)
                            lootcorpse(bot, target, instigator)
                            magicsay = str(instigator + ' uses magic on ' + target + ', killing ' + target)
                            magicnotice = str(instigator + " used a magic on you that killed you")
                        elif magicusage == 'health':
                            healthmath = int(int(targethealth) - int(targethealthstart))
                            magicsay = str(instigator + ' uses magic on ' + target + ' that increased health by ' + str(healthmath))
                            magicnotice = str(instigator + " used a magic on you that increased health by " + str(healthmath))
                        else:
                            magicsay = str(instigator + ' uses magic on ' + target + ', dealing ' + str(damage) + ' damage.')
                            magicnotice = str(instigator + ' uses magic on ' + target + ', dealing ' + str(damage) + ' damage.')
                        bot.say(str(magicsay))
                        if not inchannel.startswith("#") and target != instigator:
                            bot.notice(str(magicnotice), target)
        
        ## Loot Items usage
        elif commandused in lootitemsarray:
            uselootitem = 0
            gethowmany = get_lootitem(bot, instigator, commandused)
            if gethowmany:
                if target == instigator:
                    uselootitem = 1
                elif target.lower() not in bot.privileges[channel.lower()]:
                    bot.say("I'm not sure who that is.")
                else:
                    targetdisenable = get_disenable(bot, target)
                    if targetdisenable:
                        uselootitem = 1
                    else:
                        bot.say(target + " does not have Challenges enabled")
                if uselootitem == 1:
                    use_lootitem(bot, instigator, target, inchannel, commandused)
            else:
                bot.say('You do not have a ' +  commandused + ' to use!')
    
        ## Combat
        else:
            target = trigger.group(3)
            targetsplit = trigger.group(3)
            lastfought = get_lastfought(bot, instigator)
            if target == 'random':
                if not lastfought:
                    lastfought = instigator
                randomtargetarray = []
                for u in bot.channels[channel].users:
                    target = u
                    if target != instigator and target != bot.nick:
                        if target != lastfought or bot.nick.endswith('dev'):
                            targetdisenable = get_disenable(bot, target)
                            targettime = get_timesince(bot, target)
                            targetspicebotdisenable = get_spicebotdisenable(bot, target)
                            targetspicebotdisenable = get_spicebotdisenable(bot, target)
                            if targetdisenable and targettime > TIMEOUT and targetspicebotdisenable or bot.nick.endswith('dev'):
                                randomtargetarray.append(target)
                if randomtargetarray == []:
                    target = 'randomfailed'
                else:
                    randomselected = random.randint(0,len(randomtargetarray) - 1)
                    target = str(randomtargetarray [randomselected])
            instigatortime = get_timesince(bot, instigator)
            targettime = get_timesince(bot, target)
            channeltime = get_timesince(bot, ALLCHAN)
            targetspicebotdisenable = get_spicebotdisenable(bot, target)
            instigatordisenable = get_disenable(bot, instigator)
            targetdisenable = get_disenable(bot, target)
            if not inchannel.startswith("#"):
                bot.say('Duels must be in channel')
            elif not target:
                bot.notice(instigator + ", Who did you want to fight?", instigator)
            elif target == 'randomfailed':
                bot.notice(instigator + ", Random Selector Failed.", instigator)
            elif target == bot.nick:
                bot.say("I refuse to fight a biological entity!")
            elif target == instigator:
                bot.say("If you are feeling self-destructive, there are places you can call.")
            elif target == lastfought and not bot.nick.endswith('dev'):
                bot.notice(instigator + ', You may not fight the same person twice in a row.', instigator)
            elif target.lower() not in bot.privileges[channel.lower()]:
                bot.say("I'm not sure who that is.")
            elif not targetspicebotdisenable:
                bot.notice(instigator + ', It looks like ' + target + ' has disabled Spicebot.', instigator)
            elif not instigatordisenable:
                bot.notice(instigator + ", It looks like you have disabled Challenges. Run .challenge on to re-enable.", instigator)
            elif not targetdisenable:
                bot.notice(instigator + ', It looks like ' + target + ' has disabled Challenges.', instigator)
            elif not instigatordisenable:
                bot.notice(instigator + ", It looks like you have disabled Challenges. Run .challenge on to re-enable.", instigator)
            elif not targetdisenable:
                bot.notice(instigator + ', It looks like ' + target + ' has disabled Challenges.', instigator)
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
            else:
                ## Announce Combat
                announcecombatmsg = str(instigator + " versus " + target)
       
                ## Check new player health
                instigatorhealth = get_health(bot, instigator)
                if not instigatorhealth:
                    fresh_health(bot, instigator)
                targethealth = get_health(bot, target)
                if not targethealth:
                    fresh_health(bot, target)

                ## Damage Done
                damage = damagedone(bot)

                ## Select Winner
                winner, loser = getwinner(bot, instigator, target)

                ## Weapon Select
                weapon = str(fullcommandused.split(targetsplit, 1)[1]).strip()
                if not weapon or winner == target:
                    weapon = weaponofchoice(bot, winner)
                weapon = weaponformatter(bot, weapon)
           
                ## Update Wins and Losses
                update_wins(bot, winner)
                update_losses(bot, loser)
            
                ## Update XP points
                XPearnedwinner = '5'
                XPearnedloser = '3'
                update_xp(bot, winner, XPearnedwinner)
                update_xp(bot, loser, XPearnedloser)
                
                ## Update last fought
                set_lastfought(bot, instigator, target)
                set_lastfought(bot, target, instigator)
            
                ## Update Health Of Loser, respawn, allow winner to loot
                currenthealth = update_health(bot, loser, damage)
                if currenthealth <= 0:
                    winnermsg = str(winner + ' killed ' + loser + " with " + weapon + ' forcing a respawn!!')
                    update_respawn(bot, loser)
                    respawn_mana(bot, loser)
                    update_kills(bot, winner)
                    ## Loot Corpse
                    lootcorpse(bot, loser, winner)
                else:
                    winnermsg = str(winner + " hits " + loser + " with " + weapon + ', dealing ' + damage + ' damage.')
            
                ## Random Inventory gain
                lootwinnermsg = ''
                lootwinnermsgb = ''
                randominventoryfind = randominventory()
                if randominventoryfind == 'true':
                    loot, loot_text = determineloottype(bot, winner)
                    add_lootitem(bot, winner, loot)
                    lootwinnermsg = str(instigator + ' found a ' + str(loot) + ' ' + str(loot_text))
                    if winner == target:
                        lootwinnermsgb = str(winner + " gains the " + str(loot))
                               
                ## On Screen Text
                bot.say(str(announcecombatmsg) + "       " + str(lootwinnermsg))
                bot.say(str(winnermsg)+ "       " + str(lootwinnermsgb))
        
                ## Update Time Of Combat
                update_time(bot, instigator)
                update_time(bot, target)
                update_time(bot, ALLCHAN)

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
    bot.db.set_nick_value(nick, 'challenges_timeout', now)
    
def get_timesince(bot, nick):
    now = time.time()
    last = bot.db.get_nick_value(nick, 'challenges_timeout') or 0
    return abs(now - int(last))

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
     
def respawn_mana(bot, nick):
    bot.db.set_nick_value(nick, 'challenges_mana', '')
    
###############
## Inventory ##
###############

def get_backpackitems(bot, target):
    totalbackpack = 0
    for x in lootitemsarray:
        gethowmany = get_lootitem(bot, target, x)
        totalbackpack = int(int(totalbackpack) + int(gethowmany))
    return totalbackpack

## maybe add a dice roll later
def randominventory():
    randomfindchance = randint(1, 120)
    if randomfindchance >= 90:
        randominventoryfind = 'true'
    else:
        randominventoryfind = 'false'
    return randominventoryfind

def determineloottype(bot, nick): 
    loot = random.randint(0,len(lootitemsarray) - 1)
    loot = str(lootitemsarray [loot])
    loot_text = get_lootitem_text(bot, nick, loot)
    return loot, loot_text

def lootcorpse(bot, loser, winner):
    for x in lootitemsarray:
        gethowmany = get_lootitem(bot, loser, x)
        databasecolumn = str('challenges_' + x)
        if gethowmany:
            bot.db.set_nick_value(loser, databasecolumn, '')
            gethowmanyb = get_lootitem(bot, winner, x)
            bot.db.set_nick_value(winner, databasecolumn, int(gethowmany) + int(gethowmanyb))

def get_lootitem(bot, nick, loottype):
    databasecolumn = str('challenges_' + loottype)
    lootitem = bot.db.get_nick_value(nick, databasecolumn) or 0
    return lootitem

def get_lootitem_text(bot, nick, loottype):
    if loottype == 'healthpotion':
        loot_text = ': worth 100 health.'
    elif loottype == 'poisonpotion':
        loot_text = ': worth -50 health.'
    elif loottype == 'manapotion':
        loot_text = ': worth 100 mana.'
    elif loottype == 'timepotion':
        loot_text = ': worth up to ' + str(TIMEOUT) + ' seconds of timeout.'
    elif loottype == 'mysterypotion':
        loot_text = ': With unknown effects!'
    else:
        loot_text = ''
    if loot_text != '':
        loot_text = str(loot_text + " Use .challenge " + str(loottype) + " to consume.")
    return loot_text
        
def use_lootitem(bot, instigator, target, inchannel, loottype):
    targethealth = get_health(bot, target)
    if not targethealth:
        fresh_health(bot, target)
    health = get_health(bot, target)
    mana = get_mana(bot, target)
    lootitem = get_lootitem(bot, instigator, loottype)
    databasecolumn = str('challenges_' + loottype)
    bot.db.set_nick_value(instigator, databasecolumn, int(lootitem) - 1)
    if target == instigator:
        mainlootusemessage = str(instigator + ' uses ' + loottype + '.')
    else:
        mainlootusemessage = str(instigator + ' uses ' + loottype + ' on ' + target + ". ")
    if loottype == 'healthpotion':
        bot.db.set_nick_value(target, 'challenges_health', int(health) + 100)
    elif loottype == 'posionpotion':
        bot.db.set_nick_value(target, 'challenges_health', int(health) - 50)
    elif loottype == 'manapotion':
        bot.db.set_nick_value(target, 'challenges_mana', int(mana) + 100)
    elif loottype == 'timepotion':
        bot.db.set_nick_value(target, 'challenges_timeout', '')
    elif loottype == 'mysterypotion':
        loot = random.randint(0,len(lootitemsarray) - 1)
        loot = str(lootitemsarray [loot])
        if loot != 'mysterypotion':
            add_lootitem(bot, instigator, loot)
            use_lootitem(bot, instigator, target, inchannel, loot)
            lootusemsg = str("a " + loot)
        else:
            nulllootitemsarray = ['water','vinegar','mud']
            nullloot = random.randint(0,len(nulllootitemsarray) - 1)
            nullloot = str(nulllootitemsarray [nullloot])
            bot.say('Looks like the Potion was just ' + str(nullloot) + ' after all.')
            lootusemsg = str("Just " + nullloot)
        mainlootusemessage = str(mainlootusemessage + ' It was ' + str(lootusemsg) + '. ')
    else:
        mainlootusemessage = str(mainlootusemessage + '')
    targethealth = get_health(bot, target)
    if targethealth <= 0:
        mainlootusemessage = str(mainlootusemessage + "This resulted in death.")
        update_respawn(bot, target)
        respawn_mana(bot, target)
        update_kills(bot, instigator)
        lootcorpse(bot, target, instigator)
    bot.say(str(mainlootusemessage))
    if not inchannel.startswith("#") and target != instigator:
        bot.notice(str(mainlootusemessage), target)
    
def add_lootitem(bot, nick, loottype):
    lootitem = get_lootitem(bot, nick, loottype)
    databasecolumn = str('challenges_' + loottype)
    bot.db.set_nick_value(nick, databasecolumn, int(lootitem) + 1)
    
######################
## Weapon Selection ##
######################

def weaponofchoice(bot, nick):
    weaponslist = get_weaponslocker(bot, nick)
    if weaponslist == []:
        weapon = "fist"
    else:
        weaponselected = random.randint(0,len(weaponslist) - 1)
        weapon = str(weaponslist [weaponselected])
    return weapon

def weaponformatter(bot, weapon):
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
    while int(instigatorfight) > 0:
        instigatorfightroll = diceroll()
        instigatorfightarray.append(instigatorfightroll)
        instigatorfight = int(instigatorfight) - 1
    instigatorfight = max(instigatorfightarray)
    while int(targetfight) > 0:
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

def get_kills(bot, nick):
    kills = bot.db.get_nick_value(nick, 'challenges_kills') or 0
    return kills

def update_kills(bot, nick):
    kills = get_kills(bot, nick)
    bot.db.set_nick_value(nick, 'challenges_kills', kills + 1)

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
    wins = int(wins)
    losses = get_losses(bot, target)
    losses = int(losses)
    if not wins and not losses:
        winlossratio = 0
    else:
        winlosstotal = abs(wins + losses)
        if winlosstotal != 0:
            winlossratio = float(wins)/winlosstotal
        else:
            winlossratio = 0
    return winlossratio

###############
## XP points ##
###############

def get_xp(bot, nick):
    xp = bot.db.get_nick_value(nick, 'challenges_xp') or 0
    return xp

def update_xp(bot, nick, XPearned):
    xp = get_xp(bot, nick)
    bot.db.set_nick_value(nick, 'challenges_xp', int(xp) + int(XPearned))
    currentxp = get_xp(bot, nick)
    return currentxp

############
## Health ##
############

def get_health(bot, nick):
    health = bot.db.get_nick_value(nick, 'challenges_health') or 0
    return health

def fresh_health(bot, nick):
    bot.db.set_nick_value(nick, 'challenges_health', '1000')

def update_health(bot, nick, damage):
    health = get_health(bot, nick)
    if not health:
        update_respawn(bot, nick)
    bot.db.set_nick_value(nick, 'challenges_health', (int(health) - int(damage)))
    currenthealth = get_health(bot, nick)
    return currenthealth

##########
## Mana ##
##########

def get_mana(bot, nick):
    mana = bot.db.get_nick_value(nick, 'challenges_mana') or 0
    return mana

def use_magicattack(bot, instigator, target, damage):
    mana = bot.db.get_nick_value(instigator, 'challenges_mana')
    bot.db.set_nick_value(instigator, 'challenges_mana', (int(mana) - 250))
    health = get_health(bot, target)
    bot.db.set_nick_value(target, 'challenges_health', (int(health) - int(damage)))

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

###################
## Last Opponent ##
###################

def get_lastfought(bot, nick):
    lastfought = bot.db.get_nick_value(nick, 'challenges_lastfought') or 0
    return lastfought

def set_lastfought(bot, nicka, nickb):
    bot.db.set_nick_value(nicka, 'challenges_lastfought', nickb)
    
###########
## Tools ##
###########

def diceroll():
    diceroll = randint(0, 20)
    return diceroll

def get_konami(bot, nick):
    konami = bot.db.get_nick_value(nick, 'challenges_konami') or 0
    return konami

def set_konami(bot, nick):
    health = get_health(bot, nick)
    bot.db.set_nick_value(nick, 'challenges_health', int(health) + 600)
    bot.db.set_nick_value(nick, 'challenges_konami', 'used')
