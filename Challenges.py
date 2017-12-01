import sopel.module
from sopel.module import OP
from sopel.module import ADMIN
from sopel.module import VOICE
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
defaultadjust = 1
TIMEOUT = 180
TIMEOUTC = 40
ALLCHAN = 'entirechannel'
OPTTIMEOUT = 1800
lootitemsarray = ['healthpotion','manapotion','poisonpotion','timepotion','mysterypotion']
challengestatsadminarray = ['opttime','wins','losses','health','mana','healthpotion','mysterypotion','timepotion','respawns','xp','kills','timeout','disenable','poisonpotion','manapotion','lastfought','konami']
challengestatsarray = ['health','mana','xp','pepper','wins','losses','winlossratio','respawns','kills','backpackitems','lastfought','timeout']
    
####################
## Main Operation ##
####################

@sopel.module.commands('challenge','duel')
def challenge_cmd(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        return mainfunction(bot, trigger)
        
def mainfunction(bot, trigger):
    
    ## Basic Vars that we will use
    instigator = trigger.nick
    inchannel = trigger.sender
    fullcommandused = trigger.group(2)
    commandortarget = trigger.group(3)
    for c in bot.channels:
        channel = c
    now = time.time()

    ## bot does not need stats or backpack items
    for x in challengestatsadminarray:
        statset = x
        if statset != 'disenable':
            set_database_value(bot, bot.nick, x, '')
            
###### Weapons migrate
    weaponsmigrate(bot, instigator)
    
    ## Make sure Opt-In time is there
    opttime = get_database_value(bot, instigator, 'opttime')
    if not opttime:
        set_database_value(bot, instigator, 'opttime', now)
    
    ## If Not a target or a command used
    if not fullcommandused:
        bot.notice(instigator + ", Who did you want to challenge? Online Docs: https://github.com/deathbybandaid/sopel-modules/blob/master/otherfiles/ChallengesDocumentation.md", instigator)
    
    ## Determine if the arg after .duel is a target or a command
    elif commandortarget.lower() not in bot.privileges[channel.lower()]:
        commandused = trigger.group(3)
        target = trigger.group(4) or trigger.nick
        targettext = trigger.group(4) or "that person"
        targetdisenable = get_database_value(bot, target, 'disenable')
        
        ## Arrays
        nontargetarray = ['everyone','add','del','inv','health','attack','instakill']
        adminonlyarray = ['statsadmin']
        privilegedarray = ['on','off']
        inchannelarray = ['random','everyone']
        
        ## Must clear these challenges to do the below functions
        if target.lower() not in bot.privileges[channel.lower()] and target not in nontargetarray and commandused != 'random' and commandused != 'everyone' and commandused != 'canifight'and target != 'random':
            bot.notice(instigator + ", It looks like " + targettext + " is either not here, or not a valid person.", instigator)
        elif not trigger.admin and commandused in adminonlyarray:
            bot.notice(instigator + "This is an admin only function.", instigator)
        elif target != instigator and not trigger.admin and commandused in privilegedarray:
            bot.notice(instigator + "This is an admin only function.", instigator)
        elif not targetdisenable and target != instigator and commandused != 'on' and commandused != 'off' and target not in nontargetarray and commandused != 'random' and commandused != 'everyone' and commandused != 'statsadmin' and target != 'random':
            bot.notice(instigator + ", It looks like " + target + " has duels off.", instigator)
        elif commandused in inchannelarray and not inchannel.startswith("#"):
            bot.notice(instigator + " Duels must be in channel.", instigator)
        elif target == bot.nick and not trigger.admin:
            bot.notice(instigator + " I cannot do that.", instigator)
            
        ## and, continue
        else:
            targetopttime = get_timesince_duels(bot, target, 'opttime')
            lastfought = get_database_value(bot, instigator, 'lastfought')
            instigatortime = get_timesince_duels(bot, instigator, 'timeout')
            targettime = get_timesince_duels(bot, target, 'timeout')
            channeltime = get_timesince_duels(bot, ALLCHAN, 'timeout')
            channellastinstigator = get_database_value(bot, ALLCHAN, 'lastinstigator')
            lastfullroomassult = get_timesince_duels(bot, ALLCHAN, 'lastfullroomassult')
            if not channellastinstigator:
                channellastinstigator = bot.nick
            if not lastfought:
                lastfought = instigator
            targetarray = []
            displaymsg = ''
            dowedisplay = 0
            
            ## Random Target
            if target == 'random':
                for u in bot.channels[channel].users:
                    cantargetduel = mustpassthesetoduel(bot, trigger, instigator, u, inchannel, channel, dowedisplay)
                    if cantargetduel and target != bot.nick:
                        targetarray.append(u)
                if targetarray == []:
                    bot.notice(instigator + ", It looks like the random target finder has failed.", instigator)
                    target = instigator
                else:
                    randomselected = random.randint(0,len(targetarray) - 1)
                    target = str(targetarray [randomselected])
                    
            ## Docs
            if commandused == 'docs' or commandused == 'help':
                bot.notice("Online Docs: https://github.com/deathbybandaid/sopel-modules/blob/master/otherfiles/ChallengesDocumentation.md", target)
            
            ## Can I fight
            elif commandused == 'canifight':
                dowedisplay = 1
                inchannel = "#bypass"
                cantargetduel = mustpassthesetoduel(bot, trigger, instigator, target, inchannel, channel, dowedisplay)
                if cantargetduel:
                    bot.notice(instigator + ", It looks like you can challenge " + target + ".", instigator)
            
            ## Duel Everyone
            elif commandused == 'everyone':
                OSDTYPE = 'notice'
                if lastfullroomassult < OPTTIMEOUT and not bot.nick.endswith('dev'):
                    bot.notice(" Full Channel Assault can't be used for %d seconds." % (OPTTIMEOUT - lastfullroomassult), instigator)
                else:
                    set_database_value(bot, ALLCHAN, 'lastfullroomassult', now)
                    for u in bot.channels[channel].users:
                        cantargetduel = mustpassthesetoduel(bot, trigger, instigator, u, inchannel, channel, dowedisplay)
                        if cantargetduel and u != bot.nick:
                            targetarray.append(u)
                    if targetarray == []:
                        bot.notice(instigator + ", It looks like the every target finder has failed.", instigator)
                    else:
                        for x in targetarray:
                            if x != instigator:
                                getreadytorumble(bot, trigger, instigator, x, OSDTYPE, channel, fullcommandused, now)
                                time.sleep(5)
                                bot.notice("  ", instigator)
                
            ## Random Dueling
            elif commandused == 'random':
                OSDTYPE = 'say'
                for u in bot.channels[channel].users:
                    cantargetduel = mustpassthesetoduel(bot, trigger, instigator, u, inchannel, channel, dowedisplay)
                    if cantargetduel:
                        targetarray.append(u)
                if targetarray == []:
                    bot.notice(instigator + ", It looks like the random target finder has failed.", instigator)
                else:
                    randomselected = random.randint(0,len(targetarray) - 1)
                    target = str(targetarray [randomselected])
                    return getreadytorumble(bot, trigger, instigator, target, OSDTYPE, channel, fullcommandused, now)

            ## On/off
            elif commandused == 'on' or commandused == 'off':
                disenablevalue = ''
                if commandused == 'on':
                    disenablevalue = 1
                if target == 'everyone':
                    for u in bot.channels[channel].users:
                        set_database_value(bot, u, 'disenable', disenablevalue)
                elif targetopttime < OPTTIMEOUT and not bot.nick.endswith('dev'):
                    bot.notice(instigator + " It looks like " + target + " can't enable/disable challenges for %d seconds." % (OPTTIMEOUT - targetopttime), instigator)
                else:
                    if targetdisenable and commandused == 'on':
                        bot.notice(instigator + ", It looks like " + target + " already has duels on.", instigator)
                    elif not targetdisenable and commandused == 'off':
                        bot.notice(instigator + ", It looks like " + target + " already has duels off.", instigator)
                    else:
                        set_database_value(bot, target, 'disenable', disenablevalue)
                        set_database_value(bot, target, 'opttime', now)
                        bot.notice(instigator + ", It looks like Challenges should be " +  commandused + ' for ' + target + '.', instigator)

            ## Who can fight
            elif commandused == 'whocanifight':
                targets = ''
                for u in bot.channels[channel.lower()].users:
                    inchannel = "#bypass"
                    cantargetduel = mustpassthesetoduel(bot, trigger, instigator, u, inchannel, channel, dowedisplay)
                    if cantargetduel and u != bot.nick and u != instigator:
                        targetarray.append(u)
                for x in targetarray:
                    if targets != '':
                        targets = str(targets + ", " + x)
                    else:
                        targets = str(x)
                chunks = targets.split()
                per_line = 15
                targetline = ''
                for i in range(0, len(chunks), per_line):
                    targetline = " ".join(chunks[i:i + per_line])
                    bot.say(str(targetline))
                if targetline == '':
                    bot.say("It looks like you cannot challenge anybody at the moment.")
                
            ## Stats
            elif commandused == 'stats':
                stats = ''
                for x in challengestatsarray:
                    if x == 'winlossratio' or x == 'backpackitems' or x == 'timeout' or x == 'pepper':
                        scriptdef = str('get_' + x + '(bot,target)')
                        gethowmany = eval(scriptdef)
                    else:
                        gethowmany = get_database_value(bot, target, x)
                    if gethowmany:
                        addstat = str(' ' + str(x) + "=" + str(gethowmany))
                        stats = str(stats + addstat)
                if stats != '':
                    stats = str(target + "'s stats:" + stats)
                    bot.notice(stats, instigator)
                else:
                    bot.notice(instigator + ", It looks like " + target + " has no stats.", instigator)

            ## Backpack
            elif commandused == 'backpack':
                backpack = ''
                for x in lootitemsarray:
                    gethowmany = get_database_value(bot, target, x)
                    if gethowmany:
                        addbackpack = str(' ' + str(x) + "=" + str(gethowmany))
                        backpack = str(backpack + addbackpack)
                totalweapons = get_database_array_total(bot, target, 'weaponslocker')
                if totalweapons:
                    addbackpack = str(" weaponstotal" + "=" + str(totalweapons))
                    backpack = str(backpack + addbackpack)
                if backpack != '':
                    backpack = str(target + "'s backpack:" + backpack)
                    bot.notice(backpack, instigator)
                else:
                    bot.notice(instigator + ", It looks like " + target + " has no backpack items.", instigator)

            ## Stats Admin
            elif commandused == 'statsadmin' and trigger.admin:
                statsadminarray = ['set','reset']
                commandtrimmed = trigger.group(5)
                statset = trigger.group(6)
                newvalue = str(fullcommandused.split(statset, 1)[1]).strip()
                if commandtrimmed not in statsadminarray:
                    bot.notice(instigator + ", A correct command use is .duel statsadmin target set/reset stat", instigator)
                elif statset not in challengestatsadminarray and statset != 'all':
                    bot.notice(instigator + ", A correct command use is .duel statsadmin target set/reset stat", instigator)
                elif commandtrimmed == 'set' and not newvalue:
                    bot.notice(instigator + ", A correct command use is .duel statsadmin target set/reset stat", instigator)
                else:
                    if not newvalue:
                        newvalue = ''
                    if target == 'everyone':
                        for u in bot.channels[channel].users:
                            etarget = u
                            if statset == 'all':
                                for x in challengestatsadminarray:
                                    set_database_value(bot, etarget, x, newvalue)
                            else:
                                set_database_value(bot, etarget, statset, newvalue)
                    else:
                        if statset == 'all':
                            for x in challengestatsadminarray:
                                set_database_value(bot, target, x, newvalue)
                                
                        else:
                            set_database_value(bot, target, statset, newvalue)
                    bot.notice(instigator + ", Possibly done Adjusting stat(s).", instigator)

            ## Leaderboard
            elif commandused == 'leaderboard':
                leaderboardscript = ''
                currentwlrleader = ''
                currentkillsleader = ''
                currentrespawnsleader = ''
                currenthealthleader = ''
                currentwlrleadernumber = 0
                currentkillsleadernumber = 0
                currentrespawnsleadernumber = 0
                currenthealthleadernumber = 9999999999
                for u in bot.channels[channel].users:
                    target = u
                    targetdisenable = get_database_value(bot, target, 'disenable')
                    if targetdisenable and target != bot.nick:
                        winlossratio = get_winlossratio(bot,target)
                        if winlossratio > currentwlrleadernumber:
                            currentwlrleader = target
                            currentwlrleadernumber = winlossratio
                        kills = get_database_value(bot, target, 'kills')
                        if int(kills) > int(currentkillsleadernumber):
                            currentkillsleader = target
                            currentkillsleadernumber = int(kills)
                        respawns = get_database_value(bot, target, 'respawns')
                        if int(respawns) > int(currentrespawnsleadernumber):
                            currentrespawnsleader = target
                            currentrespawnsleadernumber = int(respawns)
                        health = get_database_value(bot, target, 'health')
                        if int(health) < int(currenthealthleadernumber):
                            currenthealthleader = target
                            currenthealthleadernumber = int(health)
                if currentwlrleadernumber > 0:
                    currentwlrleadernumber = format(currentwlrleadernumber, '.3f')
                    leaderboardscript = str(leaderboardscript + "Wins/Losses: " + currentwlrleader + " at " + str(currentwlrleadernumber) + ".     ")
                if currentkillsleadernumber > 0:
                    leaderboardscript = str(leaderboardscript + "Top Killer: " + currentkillsleader + " with " + str(currentkillsleadernumber) + " kills.     ")
                if currentrespawnsleadernumber > 0:
                    leaderboardscript = str(leaderboardscript + "Top Killed: " + currentrespawnsleader + " with " + str(currentrespawnsleadernumber) + " respawns.     ")
                if currenthealthleadernumber > 0:
                    leaderboardscript = str(leaderboardscript + "Closest To Death: " + currenthealthleader + " with " + str(currenthealthleadernumber) + " health.     ")
                if leaderboardscript == '':
                    leaderboardscript = str("Leaderboard appears to be empty")
                bot.say(leaderboardscript)

            ## Loot Items usage
            elif commandused in lootitemsarray:
                uselootitem = 0
                gethowmany = get_database_value(bot, instigator, commandused)
                if gethowmany:
                    saymsg = 'true'
                    use_lootitem(bot, instigator, target, inchannel, commandused, saymsg)
                else:
                    bot.notice(instigator + ", You do not have a " +  commandused + " to use!", instigator)
         
            ## Konami
            elif commandused == 'upupdowndownleftrightleftrightba':
                konami = get_database_value(bot, target, 'konami')
                if not konami:
                    set_database_value(bot, instigator, 'konami', 1)
                    bot.notice(instigator + " you have found the cheatcode easter egg!!!", instigator)
                else:
                    bot.notice(instigator + " you can only cheat once.", instigator)
                
            ## Weaponslocker
            elif commandused == 'weaponslocker':
                weaponslist = get_database_value(bot, instigator, 'weaponslocker') or []
                adjustmentdirection = trigger.group(4)
                if not adjustmentdirection:
                    bot.say('Use .duel weaponslocker add/del to adjust Locker Inventory.')
                elif adjustmentdirection == 'inv':
                    weapons = ''
                    for x in weaponslist:
                        weapon = x
                        if weapons != '':
                            weapons = str(weapons + ", " + weapon)
                        else:
                            weapons = str(weapon)
                    chunks = weapons.split()
                    per_line = 15
                    weaponline = ''
                    for i in range(0, len(chunks), per_line):
                        weaponline = " ".join(chunks[i:i + per_line])
                        bot.notice(str(weaponline), instigator)
                    if weaponline == '':
                        bot.say('You do not appear to have anything in your weapons locker! Use .duel weaponslocker add/del to adjust Locker Inventory.')
                else:
                    weaponchange = str(fullcommandused.split(adjustmentdirection, 1)[1]).strip()
                    if not weaponchange:
                        bot.say("What weapon would you like to add/remove?")
                    else:
                        if weaponchange in weaponslist and adjustmentdirection == 'add':
                            weaponlockerstatus = 'already'
                        elif weaponchange not in weaponslist and adjustmentdirection == 'del':
                            weaponlockerstatus = 'already not'
                        else:
                            if adjustmentdirection == 'add':
                                weaponlockerstatus = 'now'
                            elif adjustmentdirection == 'del':
                                weaponlockerstatus = 'no longer'
                            adjust_database_array(bot, instigator, weaponchange, 'weaponslocker', adjustmentdirection)
                        message = str(weaponchange + " is " + weaponlockerstatus + " in your weapons locker.")
                        bot.say(message)
        
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
                    mana = get_database_value(bot, instigator, 'mana')
                    if magicusage == 'attack':
                        manarequired = -250
                        damage = -200
                    elif magicusage == 'health':
                        manarequired = -200
                        damage = 200
                    elif magicusage == 'instakill':
                        manarequired = -1550
                        damage = -99999
                    damagetext = abs(damage)
                    if not mana:
                        bot.notice(instigator + " you don't have any mana.", instigator)
                    elif mana < manarequired:
                        manamath = int(manarequired - mana)
                        bot.notice(instigator + " you need " + str(manamath) + " more mana to do this attack.", instigator)
                    else:
                        if target.lower() not in bot.privileges[channel.lower()]:
                            bot.say("I'm not sure who that is.")
                        elif target == bot.nick:
                            bot.say("I am immune to that kind of attack.")
                        else:
                            targethealthstart = get_database_value(bot, target, 'health')
                            adjust_database_value(bot, instigator, 'mana', manarequired)
                            adjust_database_value(bot, target, 'health', damage)
                            targethealth = get_database_value(bot, target, 'health')
                            if targethealth <= 0:
                                whokilledwhom(bot, instigator, target)
                                magicsay = str(instigator + ' uses magic on ' + target + ', killing ' + target)
                                magicnotice = str(instigator + " used a magic on you that killed you")
                            elif magicusage == 'health':
                                healthmath = int(int(targethealth) - int(targethealthstart))
                                magicsay = str(instigator + ' uses magic on ' + target + ' that increased health by ' + str(healthmath))
                                magicnotice = str(instigator + " used a magic on you that increased health by " + str(healthmath))
                            else:
                                magicsay = str(instigator + ' uses magic on ' + target + ', dealing ' + str(damagetext) + ' damage.')
                                magicnotice = str(instigator + ' uses magic on ' + target + ', dealing ' + str(damagetext) + ' damage.')
                            bot.say(str(magicsay))
                            if not inchannel.startswith("#") and target != instigator:
                                bot.notice(str(magicnotice), target)
                    mana = get_database_value(bot, instigator, 'mana')
                    if mana <= 0:
                        set_database_value(bot, instigator, 'mana', '')
                                
            else:
                bot.notice(instigator + ", It looks like that is either not here, or not a valid person.", instigator)
    else:
        OSDTYPE = 'say'
        target = trigger.group(3)
        dowedisplay = 1
        executedueling = mustpassthesetoduel(bot, trigger, instigator, target, inchannel, channel, dowedisplay)
        if executedueling:
            return getreadytorumble(bot, trigger, instigator, target, OSDTYPE, channel, fullcommandused, now)
    
    ## bot does not need stats or backpack items
    for x in challengestatsadminarray:
        statset = x
        if statset != 'disenable':
            set_database_value(bot, bot.nick, x, '')
        
def getreadytorumble(bot, trigger, instigator, target, OSDTYPE, channel, fullcommandused, now):
    
    ## Weapons migrate
    weaponsmigrate(bot, instigator)
    weaponsmigrate(bot, target)
    
    ## Update Time Of Combat
    set_database_value(bot, instigator, 'timeout', now)
    set_database_value(bot, target, 'timeout', now)
    set_database_value(bot, ALLCHAN, 'timeout', now)
    
    ## Naming and Initial pepper level
    instigatorname, instigatorpepperstart = whatsyourname(bot, trigger, instigator, channel)
    if instigator == target:
        targetname = "themself"
        targetpepperstart = ''
    else:
        targetname, targetpepperstart = whatsyourname(bot, trigger, target, channel)

    ## Announce Combat
    announcecombatmsg = str(instigatorname + " versus " + targetname)
       
    ## Check for new player health
    healthcheck(bot, instigator)
    healthcheck(bot, target)
    
    ## Damage Done (random)
    damage = damagedone(bot, target)

    ## Manual weapon
    weapon = str(fullcommandused.split(trigger.group(3), 1)[1]).strip()
    if not weapon:
        manualweapon = 'false'
    else:
        manualweapon = 'true'
        if weapon == 'allchan':
            weapon = getallchanweaponsrandom(bot, instigator, channel)
        
    ## Select Winner
    if target == bot.nick:
        winner = bot.nick
        loser = instigator
    else:
        winner, loser = getwinner(bot, instigator, target, manualweapon)

    ## Weapon Select
    if manualweapon == 'false' or winner == target:
        if winner == bot.nick:
            weapon = ''
        else:
            weapon = weaponofchoice(bot, winner)
    weapon = weaponformatter(bot, weapon)
           
    ## Update Wins and Losses
    if instigator != target:
        adjust_database_value(bot, winner, 'wins', defaultadjust)
        adjust_database_value(bot, loser, 'losses', defaultadjust)
            
    ## Update XP points
    XPearnedwinner = '5'
    XPearnedloser = '3'
    if instigator != target:
        adjust_database_value(bot, winner, 'xp', XPearnedwinner)
        adjust_database_value(bot, loser, 'xp', XPearnedloser)
                
    ## Update last fought
    if instigator != target:
        set_database_value(bot, instigator, 'lastfought', target)
        set_database_value(bot, target, 'lastfought', instigator)
    
    ## Same person can't instigate twice in a row
    set_database_value(bot, ALLCHAN, 'lastinstigator', instigator)
            
    ## Update Health Of Loser, respawn, allow winner to loot
    adjust_database_value(bot, loser, 'health', damage)
    damage = abs(damage)
    currenthealth = get_database_value(bot, loser, 'health')
    if currenthealth <= 0:
        whokilledwhom(bot, winner, loser)
        if instigator == target:
            loser = targetname
        winnermsg = str(winner + ' killed ' + loser + " with " + weapon + ' forcing a respawn!!')
    else:
        if instigator == target:
            loser = targetname
        winnermsg = str(winner + " hits " + loser + " " + weapon + ', dealing ' + str(damage) + ' damage.')
        
    ## new pepper level?
    pepperstatuschangemsg = ''
    instigatorpeppernow = get_pepper(bot, instigator)
    targetpeppernow = get_pepper(bot, target)
    if instigatorpeppernow != instigatorpepperstart and instigator != target:
        pepperstatuschangemsg = str(pepperstatuschangemsg + instigator + " graduates to " + instigatorpeppernow + "! ")
    if targetpeppernow != targetpepperstart and instigator != target:
        pepperstatuschangemsg = str(pepperstatuschangemsg + target + " graduates to " + targetpeppernow + "! ")
            
    ## Random Inventory gain
    lootwinnermsg = ''
    lootwinnermsgb = ''
    randominventoryfind = randominventory()
    if randominventoryfind == 'true' and target != bot.nick and instigator != target:
        loot = determineloottype(bot, winner)
        loot_text = get_lootitem_text(bot, winner, loot)
        adjust_database_value(bot, winner, loot, defaultadjust)
        lootwinnermsg = str(instigator + ' found a ' + str(loot) + ' ' + str(loot_text))
        if winner == target:
            lootwinnermsgb = str(winner + " gains the " + str(loot))
                               
    ## On Screen Text
    if OSDTYPE == 'say':
        bot.say(str(announcecombatmsg) + "       " + str(lootwinnermsg))
        bot.say(str(winnermsg)+ "       " + str(lootwinnermsgb))
        if instigatorpeppernow != instigatorpepperstart or targetpeppernow != targetpepperstart:
            bot.say(pepperstatuschangemsg)
    elif OSDTYPE == 'notice':
        bot.notice(str(announcecombatmsg) + "       " + str(lootwinnermsg), winner)
        bot.notice(str(announcecombatmsg) + "       " + str(lootwinnermsg), loser)
        bot.notice(str(winnermsg)+ "       " + str(lootwinnermsgb), winner)
        bot.notice(str(winnermsg)+ "       " + str(lootwinnermsgb), loser)
        if instigatorpeppernow != instigatorpepperstart or targetpeppernow != targetpepperstart:
            bot.notice(pepperstatuschangemsg, winner)
            bot.notice(pepperstatuschangemsg, loser)
    else:
        bot.say('Looks Like Something went wrong!')
        
        
## 30 minute automation
# health regen
# mysterypotion
# reset last instigator
@sopel.module.interval(1800)
def healthregen(bot):
    
    ## bot does not need stats or backpack items
    for x in challengestatsadminarray:
        statset = x
        if statset != 'disenable':
            set_database_value(bot, bot.nick, x, '')
    
    ## Clear Last Instigator
    set_database_value(bot, ALLCHAN, 'lastinstigator', '')
    
    ## Who gets to win a mysterypotion?
    randomtargetarray = []
    lasttimedlootwinner = get_database_value(bot, ALLCHAN, 'lasttimedlootwinner')
    if not lasttimedlootwinner:
        lasttimedlootwinner = bot.nick
    for channel in bot.channels:
        for u in bot.privileges[channel.lower()]:
            target = u
            targetdisenable = get_database_value(bot, target, 'disenable')
            if targetdisenable and target != lasttimedlootwinner and target != bot.nick:
                health = get_database_value(bot, target, 'health')
                if health < 500:
                    adjust_database_value(bot, target, 'health', '50')
                randomtargetarray.append(target)
        if randomtargetarray == []:
            dummyvar = 1
        else:
            randomselected = random.randint(0,len(randomtargetarray) - 1)
            target = str(randomtargetarray [randomselected])
            loot = 'mysterypotion'
            loot_text = get_lootitem_text(bot, target, loot)
            adjust_database_value(bot, target, loot, defaultadjust)
            lootwinnermsg = str(target + ' is awarded a ' + str(loot) + ' ' + str(loot_text))
            bot.notice(lootwinnermsg, target)
            set_database_value(bot, ALLCHAN, 'lasttimedlootwinner', target)
            
        
## Functions######################################################################################################################

######################
## Criteria to duel ##
######################

def mustpassthesetoduel(bot, trigger, instigator, target, inchannel, channel, dowedisplay):
    executedueling = 0
    lastfought = get_database_value(bot, instigator, 'lastfought')
    targetspicebotdisenable = get_botdatabase_value(bot, target, 'disenable')
    instigatordisenable = get_database_value(bot, instigator, 'disenable')
    targetdisenable = get_database_value(bot, target, 'disenable')
    instigatortime = get_timesince_duels(bot, instigator, 'timeout')
    targettime = get_timesince_duels(bot, target, 'timeout')
    channeltime = get_timesince_duels(bot, ALLCHAN, 'timeout')
    channellastinstigator = get_database_value(bot, ALLCHAN, 'lastinstigator')
    if not channellastinstigator:
        channellastinstigator = bot.nick
    
    if not inchannel.startswith("#"):
        displaymsg = str(instigator + " Duels must be in channel.")
    elif target.lower() not in bot.privileges[channel.lower()]:
        displaymsg = str(instigator + ", It looks like that is either not here, or not a valid person.")
    elif target == bot.nick and not targetdisenable:
        displaymsg = str(instigator + " I refuse to fight a biological entity!")
    elif instigator == channellastinstigator and not bot.nick.endswith('dev'):
        displaymsg = str(instigator + ', You may not instigate fights twice in a row within a half hour.')
    elif target == lastfought and not bot.nick.endswith('dev'):
        displaymsg = str(instigator + ', You may not fight the same person twice in a row.')
    elif not targetspicebotdisenable and target != bot.nick:
        displaymsg = str(instigator + ', It looks like ' + target + ' has disabled ' + bot.nick + "." )
    elif not instigatordisenable:
        displaymsg = str(instigator + ", It looks like you have disabled Challenges. Run .challenge on to re-enable.")
    elif not targetdisenable:
        displaymsg = str(instigator + ', It looks like ' + target + ' has disabled Challenges.')
    elif instigatortime < TIMEOUT and not bot.nick.endswith('dev'):
        displaymsg = str("You can't challenge for %d seconds." % (TIMEOUT - instigatortime))
    elif targettime < TIMEOUT and not bot.nick.endswith('dev'):
        displaymsg = str(target + " can't challenge for %d seconds." % (TIMEOUT - targettime))
    elif channeltime < TIMEOUTC and not bot.nick.endswith('dev'):
        displaymsg = str(channel + " can't challenge for %d seconds." % (TIMEOUTC - channeltime))
    else:
        displaymsg = ''
        executedueling = 1
    if dowedisplay:
        bot.notice(displaymsg, instigator)
    return executedueling

##############
## Database ##
##############

def get_database_value(bot, nick, databasekey):
    databasecolumn = str('challenges_' + databasekey)
    database_value = bot.db.get_nick_value(nick, databasecolumn) or 0
    return database_value

def set_database_value(bot, nick, databasekey, value):
    databasecolumn = str('challenges_' + databasekey)
    bot.db.set_nick_value(nick, databasecolumn, value)
    
def adjust_database_value(bot, nick, databasekey, value):
    oldvalue = get_database_value(bot, nick, databasekey)
    databasecolumn = str('challenges_' + databasekey)
    bot.db.set_nick_value(nick, databasecolumn, int(oldvalue) + int(value))
   
def get_database_array_total(bot, nick, databasekey):
    array = get_database_value(bot, nick, databasekey) or []
    entriestotal = len(array)
    return entriestotal

def adjust_database_array(bot, nick, entry, databasekey, adjustmentdirection):
    adjustarray = get_database_value(bot, nick, databasekey) or []
    adjustarraynew = []
    for x in adjustarray:
        adjustarraynew.append(x)
    set_database_value(bot, nick, databasekey, '')
    adjustarray = []
    if adjustmentdirection == 'add':
        adjustarraynew.append(entry)
    elif adjustmentdirection == 'del':
        adjustarraynew.remove(entry)
    for x in adjustarraynew:
        if x not in adjustarray:
            adjustarray.append(x)
    if adjustarray == []:
        set_database_value(bot, nick, databasekey, '')
    else:
        set_database_value(bot, nick, databasekey, adjustarray)
    
###################
## Living Status ##
###################

def whokilledwhom(bot, winner, loser):
    ## Reset mana and health
    set_database_value(bot, loser, 'mana', '')
    set_database_value(bot, loser, 'health', '1000')
    ## update kills/deaths
    adjust_database_value(bot, winner, 'kills', defaultadjust)
    adjust_database_value(bot, loser, 'respawns', defaultadjust)
    ## Loot Corpse
    for x in lootitemsarray:
        gethowmany = get_database_value(bot, loser, x)
        adjust_database_value(bot, winner, x, gethowmany)
        set_database_value(bot, loser, x, '')

def healthcheck(bot, nick):
    health = get_database_value(bot, nick, 'health')
    if not health and nick != bot.nick:
        set_database_value(bot, nick, 'health', '1000')

##########
## Time ##
##########
    
def get_timesince_duels(bot, nick, databasekey):
    now = time.time()
    last = get_database_value(bot, nick, databasekey) or 0
    return abs(now - int(last))

def get_timeout(bot, nick):
    time_since = get_timesince_duels(bot, nick, 'timeout')
    if time_since < TIMEOUT:
        timediff = int(TIMEOUT - time_since)
    else:
        timediff = 0
    return timediff

###########
## Names ##
###########

def whatsyourname(bot, trigger, nick, channel):
    nickname = str(nick)
    
    ## Pepper Level
    pepperstart = get_pepper(bot, nick)
    
    ## Is user Special?
    botownerarray = []
    operatorarray = []
    voicearray = []
    adminsarray = []
    for u in bot.channels[channel.lower()].users:
        nametargetdisenable = get_database_value(bot, u, 'disenable')
        if u != bot.nick and nametargetdisenable:
            nametarget = u
            if nametarget.lower() in bot.config.core.owner.lower():
                botownerarray.append(nametarget)
            if bot.privileges[channel.lower()][nametarget] == OP:
                operatorarray.append(nametarget)
            if bot.privileges[channel.lower()][nametarget.lower()] == VOICE:
                voicearray.append(nametarget)
            if nametarget in bot.config.core.admins:
                adminsarray.append(nametarget)
    
    ## Is nick Special?
    if nick in botownerarray:
        nickname = str("The Legendary " + nickname)
    elif nick in operatorarray:
        nickname = str("The Magnificent " + nickname)
    elif nick in voicearray:
        nickname = str("The Incredible " + nickname)
    elif nick in adminsarray:
        nickname = str("The Valient " + nickname)
    else:
        nickname = str(nickname)
        
    ## Pepper Names
    if pepperstart != '':
        nickname = str(nickname + " (" + pepperstart + ")")
    else:
        nickname = str(nickname + " (n00b)")
    
    return nickname, pepperstart
    
###############
## Inventory ##
###############

def get_backpackitems(bot, target):
    totalbackpack = 0
    for x in lootitemsarray:
        gethowmany = get_database_value(bot, target, x)
        totalbackpack = int(int(totalbackpack) + int(gethowmany))
    return totalbackpack

## maybe add a dice roll later
def randominventory():
    randomfindchance = diceroll(120)
    randominventoryfind = 'false'
    if randomfindchance >= 90:
        randominventoryfind = 'true'
    return randominventoryfind

def determineloottype(bot, nick):
    loot = random.randint(0,len(lootitemsarray) - 1)
    loot = str(lootitemsarray [loot])
    return loot

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
        
def use_lootitem(bot, instigator, target, inchannel, loottype, saymsg):
    targethealth = get_database_value(bot, target, 'health')
    if not targethealth:
        set_database_value(bot, target, 'health', '1000')
        targethealth = get_database_value(bot, target, 'health')
    gethowmany = get_database_value(bot, target, 'mana')
    adjust_database_value(bot, instigator, loottype, -1)
    mana = get_database_value(bot, target, 'mana')
    if target == instigator:
        mainlootusemessage = str(instigator + ' uses ' + loottype + '.')
    else:
        mainlootusemessage = str(instigator + ' uses ' + loottype + ' on ' + target + ". ")
    if loottype == 'healthpotion':
        adjust_database_value(bot, target, 'health', '100')
    elif loottype == 'poisonpotion':
        adjust_database_value(bot, target, 'health', '-50')
    elif loottype == 'manapotion':
        adjust_database_value(bot, target, 'mana', '100')
    elif loottype == 'timepotion':
        channellastinstigator = get_database_value(bot, ALLCHAN, 'lastinstigator')
        if not channellastinstigator:
            channellastinstigator = bot.nick
        if channellastinstigator == target:
            set_database_value(bot, ALLCHAN, 'lastinstigator', '')
        set_database_value(bot, target, 'timeout', '')
        set_database_value(bot, ALLCHAN, 'timeout', '')
    elif loottype == 'mysterypotion':
        loot = random.randint(0,len(lootitemsarray) - 1)
        loot = str(lootitemsarray [loot])
        if loot != 'mysterypotion':
            adjust_database_value(bot, instigator, loot, defaultadjust)
            saymsg = 'false'
            use_lootitem(bot, instigator, target, inchannel, loot, saymsg)
            saymsg = 'true'
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
    targethealth = get_database_value(bot, target, 'health')
    if targethealth <= 0:
        mainlootusemessage = str(mainlootusemessage + "This resulted in death.")
        whokilledwhom(bot, instigator, target)
    if saymsg == 'true':
        bot.say(str(mainlootusemessage))
        if not inchannel.startswith("#") and target != instigator:
            bot.notice(str(mainlootusemessage), target)
    
######################
## Weapon Selection ##
######################

## allchan weapons
def getallchanweaponsrandom(bot, nick, channel):
    lastusedweapon = get_database_value(bot, nick, 'lastweaponused')
    allchanweaponsarray = getallchanweapons(bot, channel)
    if not lastusedweapon:
        lastusedweapon = "fist"
    if allchanweaponsarray == []:
        weapon = "fist"
    else:
        for x in weaponslist:
            if x != lastusedweapon:
                weaponslistselect.append(x)
        if weaponslistselect == []:
            weapon = lastusedweapon
        else:
            weaponselected = random.randint(0,len(weaponslistselect) - 1)
            weapon = str(weaponslistselect [weaponselected])
    set_database_value(bot, nick, 'lastweaponused', weapon)
    return weapon
        
def getallchanweapons(bot, channel):
    allchanweaponsarray = []
    for u in bot.channels[channel].users:
        weaponslist = bot.db.get_nick_value(u, 'weapons_locker') or []
        for x in weaponslist:
            allchanweaponsarray.append(x)
    return allchanweaponsarray
        
## Hacky Patch to move weaponslocker to new database setup
def weaponsmigrate(bot, nick):
    weaponslistnew = []
    weaponslist = bot.db.get_nick_value(nick, 'weapons_locker') or []
    if weaponslist or weaponslist != []:
        for x in weaponslist:
            weaponslistnew.append(x)
        set_database_value(bot, nick, 'weaponslocker', weaponslistnew)
        bot.db.set_nick_value(nick, 'weapons_locker', '')

def weaponofchoice(bot, nick):
    weaponslistselect = []
    weaponslist = get_database_value(bot, nick, 'weaponslocker') or []
    lastusedweapon = get_database_value(bot, nick, 'lastweaponused')
    if not lastusedweapon:
        lastusedweapon = "fist"
    if weaponslist == []:
        weapon = "fist"
    else:
        for x in weaponslist:
            if x != lastusedweapon:
                weaponslistselect.append(x)
        if weaponslistselect == []:
            weapon = lastusedweapon
        else:
            weaponselected = random.randint(0,len(weaponslistselect) - 1)
            weapon = str(weaponslistselect [weaponselected])
    set_database_value(bot, nick, 'lastweaponused', weapon)
    return weapon

def weaponformatter(bot, weapon):
    if weapon == '':
        weapon = weapon
    elif weapon.lower().startswith('a ') or weapon.lower().startswith('an ') or weapon.lower().startswith('the '):
        weapon = str('with ' + weapon)
    elif weapon.split(' ', 1)[0].endswith("'s"):
        weapon = str('with ' + weapon)
    elif weapon.lower().startswith('a') or weapon.lower().startswith('e') or weapon.lower().startswith('i') or weapon.lower().startswith('o') or weapon.lower().startswith('u'):
        weapon = str('with an ' + weapon)
    else:
        weapon = str('with a ' + weapon)
    return weapon

#################
## Damage Done ##
#################

def damagedone(bot, target):
    if target == bot.nick:
        damage = -150
    else:
        rando = diceroll(120)
        damage = -abs(rando)
    return damage

##################
## Pepper level ##
##################

def get_pepper(bot, nick):
    xp = get_database_value(bot, nick, 'xp')
    if nick == bot.nick:
        pepper = 'Dragon Breath Chilli'
    elif not xp:
        pepper = ''
    elif xp > 0 and xp < 100:
        pepper = 'Pimiento'
    elif xp >= 100 and xp < 250:
        pepper = 'Sonora'
    elif xp >= 250 and xp < 500:
        pepper = 'Anaheim'
    elif xp >= 500 and xp < 1000:
        pepper = 'Poblano'
    elif xp >= 1000 and xp < 2500:
        pepper = 'Jalapeno'
    elif xp >= 2500 and xp < 5000:
        pepper = 'Serrano'
    elif xp >= 5000 and xp < 7500:
        pepper = 'Chipotle'
    elif xp >= 7500 and xp < 10000:
        pepper = 'Tabasco'
    elif xp >= 10000 and xp < 15000:
        pepper = 'Cayenne'
    elif xp >= 15000 and xp < 25000:
        pepper = 'Thai Pepper'
    elif xp >= 25000 and xp < 45000:
        pepper = 'Datil'
    elif xp >= 45000 and xp < 70000:
        pepper = 'Habanero'
    elif xp >= 70000 and xp < 100000:
        pepper = 'Ghost Chili'
    elif xp >= 100000 and xp < 250000:
        pepper = 'Mace'
    elif xp >= 250000:
        pepper = 'Pure Capsaicin'
    return pepper

###################
## Select Winner ##
###################

def getwinner(bot, instigator, target, manualweapon):
    instigatorxp = get_database_value(bot, instigator, 'xp')
    if not instigatorxp:
        instigatorxp = '1'
    targetxp = get_database_value(bot, target, 'xp')
    if not targetxp:
        targetxp = '1'
    
    instigatorkills = get_database_value(bot, instigator, 'kills')
    if not instigatorkills:
        instigatorkills = '1'
    targetkills = get_database_value(bot, target, 'kills')
    if not targetkills:
        targetkills = '1'
    
    ## each person
    instigatorfight = '1'
    targetfight = '1'
    
    # extra roll for using the weaponslocker or manual weapon usage
    instigatorweaponslist = get_database_value(bot, instigator, 'weaponslocker') or []
    if not instigatorweaponslist == [] or manualweapon == 'true':
        instigatorfight = int(instigatorfight) + 1
    targetweaponslist = get_database_value(bot, target, 'weaponslocker') or []
    if not targetweaponslist == []:
        targetfight = int(targetfight) + 1
    
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
        
    ## more kills
    if int(instigatorkills) > int(targetkills):
        instigatorfight = int(instigatorfight) + 1
    elif int(instigatorkills) < int(targetkills):
        targetfight = int(targetfight) + 1
    elif int(instigatorkills) == int(targetkills):
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
        instigatorfightroll = diceroll(20)
        instigatorfightarray.append(instigatorfightroll)
        instigatorfight = int(instigatorfight) - 1
    instigatorfight = max(instigatorfightarray)
    while int(targetfight) > 0:
        targetfightroll = diceroll(20)
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

def get_winlossratio(bot,target):
    wins = get_database_value(bot, target, 'wins')
    wins = int(wins)
    losses = get_database_value(bot, target, 'losses')
    losses = int(losses)
    if not wins or not losses:
        winlossratio = 0
    else:
        winlossratio = float(wins)/losses
    return winlossratio

###########
## Tools ##
###########

def diceroll(howmanysides):
    diceroll = randint(0, howmanysides)
    return diceroll
