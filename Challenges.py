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

###################
## Configurables ##
###################

defaultadjust = 1 ## The default number to increase a stat
USERTIMEOUT = 180 ## Time between a users ability to duel - 3 minutes
CHANTIMEOUT = 40 ## Time between duels in a channel - 40 seconds
OPTTIMEOUT = 1800 ## Time between opting in and out of the game - Half hour
ASSAULTTIMEOUT = 1800 ## Time Between Full Channel Assaults
CLASSTIMEOUT = 86400 ## Time between changing class - One Day
GITWIKIURL = "https://github.com/deathbybandaid/sopel-modules/wiki/Challenges" ## Wiki URL
changeclasscost = 100 ## ## how many coins to change class

############
## Arrays ##
############
botdevteam = ['deathbybandaid','DoubleD','Mace_Whatdo','dysonparkes','PM','under_score']
lootitemsarray = ['healthpotion','manapotion','poisonpotion','timepotion','mysterypotion']
backpackarray = ['weaponstotal','coins','healthpotion','manapotion','poisonpotion','timepotion','mysterypotion']
transactiontypesarray = ['buy','sell','trade','use']
challengestatsadminarray = ['shield','classtimeout','class','curse','bestwinstreak','worstlosestreak','opttime','coins','wins','losses','health','mana','healthpotion','mysterypotion','timepotion','respawns','xp','kills','timeout','disenable','poisonpotion','manapotion','lastfought','konami']
challengestatsarray = ['class','health','curse','shield','mana','xp','wins','losses','winlossratio','respawns','kills','backpackitems','lastfought','timeout']
classarray = ['barbarian','mage','scavenger','rogue','ranger']
statsadminchangearray = ['set','reset']
statsbypassarray = ['winlossratio','timeout']

#################
## null values ##
#################

displaymsg = ''
dowedisplay = 0
disenablevalue = ''
targets = ''
classes = ''
script = ''
stats = ''
leaderboardscript = ''
currentwlrleader = ''
currentkillsleader = ''
currentrespawnsleader = ''
currenthealthleader = ''
currentstreaksleader = ''
currentwlrleadernumber = 0
currentkillsleadernumber = 0
currentrespawnsleadernumber = 0
currenthealthleadernumber = 9999999999
currentstreaksleadernumber = 0
                
#################
## null arrays ##
#################

targetarray = []
botownerarray = []
operatorarray = []
voicearray = []
adminsarray = []
allusersinroomarray = []
dueloptedinarray = []
channelarray = []
targetcantoptarray = []
canduelarray = []
classcantchangearray = []

################################################################################
## Main Operation #### Main Operation #### Main Operation #### Main Operation ##
################################################################################

@sopel.module.commands('challenge','duel')
def execute_main(bot, trigger):
    
    ## Initial ARGS of importance
    triggerargsarray = create_args_array(trigger.group(2))
    fullcommandused = get_trigger_arg(triggerargsarray, 0)
    commandortarget = get_trigger_arg(triggerargsarray, 1)
    
    ## Build User/channel Arrays
    for c in bot.channels:
        channelarray.append(c)
        inchannel = "#bypass"
        dowedisplay = 0
        ## All Users in channel
        for u in bot.channels[c.lower()].users:
            allusersinroomarray.append(u)
            ## Users that can opt in/out of duels
            opttime = get_timesince_duels(bot, u, 'opttime')
            if opttime < OPTTIMEOUT and not bot.nick.endswith('dev'):
                targetcantoptarray.append(u)
            # Users with duels enabled
            disenable = get_database_value(bot, u, 'disenable')
            if u != bot.nick and disenable:
                dueloptedinarray.append(u)
            # Target passes all duel checks
            canduel = mustpassthesetoduel(bot, trigger, u, u, inchannel, c, dowedisplay)
            if canduel:
                canduelarray.append(u)
            ## Bot Owner (probably will only ever be one)
            if u.lower() in bot.config.core.owner.lower():
                botownerarray.append(u)
            ## Channel OP
            if bot.privileges[c.lower()][u] == OP:
                operatorarray.append(u)
            ## Channel VOICE
            if bot.privileges[c.lower()][u.lower()] == VOICE:
                voicearray.append(u)
            ## Bot Admins
            if u in bot.config.core.admins:
                adminsarray.append(u)
            classtime = get_timesince_duels(bot, u, 'classtimeout')
            if classtime < CLASSTIMEOUT and not bot.nick.endswith('dev'):
                classcantchangearray.append(u)
            
## Array Totals
    targetcantoptarraytotal = len(targetcantoptarray)
    canduelarraytotal = len(canduelarray)
    botownerarraytotal = len(botownerarray)
    operatorarraytotal = len(operatorarray)
    voicearraytotal = len(voicearray)
    adminsarraytotal = len(adminsarray)
    dueloptedinarraytotal = len(dueloptedinarray)
    allusersinroomarraytotal = len(allusersinroomarray)
    channelarraytotal = len(channelarray)
        
###### Channel (assumes only one channel,,, need to fix somehow someday)
    channel = get_trigger_arg(channelarray, 1)
    inchannel = trigger.sender
    
    ## Time when Module use started
    now = time.time()

    ## bot does not need stats or backpack items
    refreshbot(bot)
    
    ## Instigator Information
    instigator = trigger.nick
    instigatortime = get_timesince_duels(bot, instigator, 'timeout') or USERTIMEOUT
    instigatorlastfought = get_database_value(bot, instigator, 'lastfought') or instigator
    instigatorcoins = get_database_value(bot, instigator, 'coins') or 0
    instigatorclass = get_database_value(bot, instigator, 'class')

    ## Channel Information
    channeltime = get_timesince_duels(bot, channel, 'timeout') or CHANTIMEOUT
    channellastinstigator = get_database_value(bot, channel, 'lastinstigator') or bot.nick
    lastfullroomassult = get_timesince_duels(bot, channel, 'lastfullroomassult') or ASSAULTTIMEOUT
    lastfullroomassultinstigator = get_database_value(bot, channel, 'lastfullroomassultinstigator') or bot.nick
    
    ## If Not a target or a command used
    if not fullcommandused:
        bot.notice(instigator + ", Who did you want to challenge? Online Docs: " + GITWIKIURL, instigator)
    
    ## Determine if the arg after .duel is a target or a command
    elif commandortarget.lower() not in allusersinroomarray:

## Fix Me! Doesn't make any sense any more for this to be outside the "subcommands"
########## Random Target
        #if get_trigger_arg(triggerargsarray, 2) == 'random':
        #    if canduelarray == []:
        #        bot.notice(instigator + ", It looks like the random target finder has failed.", instigator)
        #    else:
        #        randomselected = random.randint(0,len(canduelarray) - 1)
        #        target = str(canduelarray [randomselected])
                
        ## Docs
        if commandortarget == 'docs' or commandortarget == 'help':
            target = get_trigger_arg(triggerargsarray, 2)
            if not target:
                bot.say("Online Docs: " + GITWIKIURL)
            elif target.lower() not in allusersinroomarray:
                bot.notice(instigator + ", It looks like " + targettext + " is either not here, or not a valid person.", instigator)
            else:
                bot.notice("Online Docs: " + GITWIKIURL, target)
        
        ## On/off
        elif commandortarget == 'on' or commandortarget == 'off':
            disenablevalue = None
            if commandortarget == 'on':
                disenablevalue = 1
            target = get_trigger_arg(triggerargsarray, 2) or instigator
            if target.lower() not in allusersinroomarray:
                bot.notice(instigator + ", It looks like " + targettext + " is either not here, or not a valid person.", instigator)
            elif target != instigator and instigator not in adminsarray:
                bot.notice(instigator + "This is an admin only function.", instigator)
            elif target == 'everyone':
                for u in allusersinroomarray:
                    set_database_value(bot, u, 'disenable', disenablevalue)
            elif target in targetcantoptarray:
                bot.notice(instigator + " It looks like " + target + " can't enable/disable challenges for %d seconds." % (OPTTIMEOUT - targetopttime), instigator)
            elif commandortarget == 'on' and target.lower() in dueloptedinarray:
                bot.notice(instigator + ", It looks like " + target + " already has duels on.", instigator)
            elif commandortarget == 'off' and target.lower() not in dueloptedinarray:
                bot.notice(instigator + ", It looks like " + target + " already has duels off.", instigator)
            else:
                set_database_value(bot, target, 'disenable', disenablevalue)
                set_database_value(bot, target, 'opttime', now)
                bot.notice(instigator + ", Challenges should now be " +  commandortarget + ' for ' + target + '.', instigator)
                        
        ## Random Dueling
        elif commandortarget == 'random':
            if canduelarray == []:
                bot.notice(instigator + ", It looks like the random target finder has failed.", instigator)
            else:
                randomselected = random.randint(0,len(canduelarray) - 1)
                target = str(canduelarray [randomselected])
                OSDTYPE = 'say'
                return getreadytorumble(bot, trigger, instigator, target, OSDTYPE, channel, fullcommandused, now, triggerargsarray)
        
        ## Duel Everyone
        elif commandortarget == 'everyone':
            if lastfullroomassult < ASSAULTTIMEOUT and not bot.nick.endswith('dev'):
                bot.notice("Full Channel Assault can't be used for %d seconds." % (ASSAULTTIMEOUT - lastfullroomassult), instigator)
            elif lastfullroomassultinstigator == instigator and not bot.nick.endswith('dev'):
                bot.notice("You may not instigate a Full Channel Assault twice in a row.", instigator)
            elif canduelarray == []:
                bot.notice(instigator + ", It looks like the Full Channel Assault target finder has failed.", instigator)
            else:
                OSDTYPE = 'notice'
                set_database_value(bot, channel, 'lastfullroomassult', now)
                set_database_value(bot, channel, 'lastfullroomassultinstigator', instigator)
                lastfoughtstart = get_database_value(bot, instigator, 'lastfought')
                for u in canduelarray:
                    if u != instigator and u != bot.nick:
                        targetlastfoughtstart = get_database_value(bot, x, 'lastfought')
                        getreadytorumble(bot, trigger, instigator, x, OSDTYPE, channel, fullcommandused, now, triggerargsarray)
                        time.sleep(5)
                        bot.notice("  ", instigator)
                        set_database_value(bot, x, 'lastfought', targetlastfoughtstart)
                set_database_value(bot, instigator, 'lastfought', lastfoughtstart)

        ## War Room
        elif commandortarget == 'warroom':
            subcommand = get_trigger_arg(triggerargsarray, 2)
            if not subcommand:
                if instigator in canduelarray:
                    bot.notice(instigator + ", It looks like you can challenge.", instigator)
                else:
                    inchannel = "#bypass"
                    dowedisplay = 1
                    mustpassthesetoduel(bot, trigger, instigator, instigator, inchannel, channel, dowedisplay)
            elif subcommand == 'assault':
                if lastfullroomassultinstigator == instigator and not bot.nick.endswith('dev'):
                    bot.notice("You may not instigate an allchan duel twice in a row.", instigator)
                elif lastfullroomassult < ASSAULTTIMEOUT and not bot.nick.endswith('dev'):
                    bot.notice(" Full Channel Assault can't be used for %d seconds." % (ASSAULTTIMEOUT - lastfullroomassult), instigator)
                else:
                    bot.notice(" Full Channel Assault can be used.", instigator)
            elif subcommand == 'list':
                for x in canduelarray:
                    if targets != '':
                        targets = str(targets + ", " + x)
                    else:
                        targets = str(x)
                bot.say(str(targets))
            elif subcommand.lower() not in allusersinroomarray:
                bot.notice(instigator + ", It looks like " + str(subcommand) + " is either not here, or not a valid person.", instigator)
            else:
                if subcommand in canduelarray:
                    bot.notice(instigator + ", It looks like you can challenge " + target + ".", instigator)
                else:
                    dowedisplay = 1
                    inchannel = "#bypass"
                    mustpassthesetoduel(bot, trigger, instigator, target, inchannel, channel, dowedisplay)

        ## Stats Admin
        elif commandortarget == 'statsadmin':
            subcommand = get_trigger_arg(triggerargsarray, 2)
            stat = get_trigger_arg(triggerargsarray, 3)
            target = get_trigger_arg(triggerargsarray, 4)
            newvalue = get_trigger_arg(triggerargsarray, 4) or ''
            if not subcommand:
                bot.notice(instigator + ", A correct command use is .duel statsadmin set/reset stat target", instigator)
            elif subcommand not in statsadminchangearray:
                bot.notice(instigator + ", A correct command use is .duel statsadmin set/reset stat target", instigator)
            elif stat not in challengestatsadminarray:
                bot.notice(instigator + ", A correct command use is .duel statsadmin set/reset stat target", instigator)
            elif target.lower() not in allusersinroomarray and target != 'everyone':
                bot.notice(instigator + ", It looks like " + str(target) + " is either not here, or not a valid person.", instigator)
            elif instigator not in adminsarray:
                bot.notice(instigator + "This is an admin only function.", instigator)
            else:
                if subcommand == 'reset':
                    newvalue = ''
                if subcommand == 'set' and newvalue != '':
                    bot.notice(instigator + ", A correct command use is .duel statsadmin set/reset stat target", instigator)
                elif target == 'everyone':
                    for u in bot.channels[channel].users:
                        if statset == 'all':
                            for x in challengestatsadminarray:
                                set_database_value(bot, u, x, newvalue)
                        else:
                            set_database_value(bot, u, statset, newvalue)
                    bot.notice(instigator + ", Possibly done Adjusting stat(s).", instigator)
                else:
                    if statset == 'all':
                        for x in challengestatsadminarray:
                            set_database_value(bot, target, x, newvalue)
                    else:
                        set_database_value(bot, target, statset, newvalue)
                    bot.notice(instigator + ", Possibly done Adjusting stat(s).", instigator)

        ## Class
        elif commandortarget == 'class':
            subcommandarray = ['set','change']
            for x in classarray:
                if classes != '':
                    classes = str(classes + ", " + x)
                else:
                    classes = str(x)
            subcommand = get_trigger_arg(triggerargsarray, 2)
            setclass = get_trigger_arg(triggerargsarray, 3)
            if not instigatorclass and not subcommand:
                bot.say("You don't appear to have a class set. Options are : " + classes + ". Run .duel class set    to set your class.")
            elif not subcommand:
                bot.say("Your class is currently set to " + str(instigatorclass) + ". Use .duel class change    to change class. Options are : " + classes + ".")
            elif instigator in classcantchangearray and not bot.nick.endswith('dev'):
                bot.say("You may not change your class more than once per day.")
            elif subcommand not in subcommandarray:
                bot.say("Invalid command. Options are set or change.")
            elif not setclass:
                bot.say("Which class would you like to use? Options are: " + classes +".")
            elif subcommand == 'set' and instigatorclass:
                bot.say("Your class is currently set to " + str(instigatorclass) + ". Use .duel class change    to change class. Options are : " + classes + ".")
            elif subcommand == 'change' and instigatorcoins < changeclasscost:
                bot.say("Changing class costs " + str(changeclasscost) + " coins.")
            elif subcommand == 'change' and setclass == instigatorclass:
                bot.say('Your class is already set to ' +  setclass)
            else:
                if setclass not in classarray:
                    bot.say("Invalid class. Options are: " + classes +".")
                else:
                    set_database_value(bot, instigator, 'class', setclass)
                    bot.say('Your class is now set to ' +  setclass)
                    set_database_value(bot, instigator, 'classtimeout', now)
                    if subcommand == 'change':
                        adjust_database_value(bot, instigator, 'coins', -abs(changeclasscost))

        ## Streaks
        elif commandortarget == 'streaks':
            target = get_trigger_arg(triggerargsarray, 2) or instigator
            if target.lower() not in allusersinroomarray:
                bot.notice(instigator + ", It looks like " + targettext + " is either not here, or not a valid person.", instigator)
            elif target.lower() not in dueloptedinarray:
                bot.notice(instigator + ", It looks like " + target + " has duels off.", instigator)
            else:
                streak_type = get_database_value(bot, target, 'currentstreaktype') or 'none'
                best_wins = get_database_value(bot, target, 'bestwinstreak') or 0
                worst_losses = get_database_value(bot, target, 'worstlosestreak') or 0
                if streak_type == 'win':
                    streak_count = get_database_value(bot, target, 'currentwinstreak') or 0
                    typeofstreak = 'winning'
                elif streak_type == 'loss':
                    streak_count = get_database_value(bot, target, 'currentlosestreak') or 0
                    typeofstreak = 'losing'
                else:
                    streak_count = 0
                if streak_count > 1 and streak_type != 'none':
                    script = str(script + "Currently on a " + typeofstreak + " streak of " + str(streak_count) + ".     ")
                if int(best_wins) > 1:
                    script = str(script + "Best Win streak= " + str(best_wins) + ".     ")
                if int(worst_losses) > 1:
                    script = str(script + "Worst Losing streak= " + str(worst_losses) + ".     ")
                if script == '':
                    bot.say(target + " has no streaks.")
                else:
                    bot.say(target + "'s streaks: " + script)
            
        ## Backpack
        elif commandortarget == 'backpack':
            target = get_trigger_arg(triggerargsarray, 2) or instigator
            if target.lower() not in allusersinroomarray:
                bot.notice(instigator + ", It looks like " + targettext + " is either not here, or not a valid person.", instigator)
            elif target.lower() not in dueloptedinarray:
                bot.notice(instigator + ", It looks like " + target + " has duels off.", instigator)
            else:
                for x in backpackarray:
                    if x == 'weaponstotal':
                        gethowmany = get_database_array_total(bot, target, 'weaponslocker')
                    else:
                        gethowmany = get_database_value(bot, target, x)
                    if gethowmany:
                        addstat = str(' ' + str(x) + "=" + str(gethowmany))
                        stats = str(stats + addstat)
                if stats != '':
                    stats = str(target + "'s " + commandortarget + ":" + stats)
                    bot.say(stats)
                else:
                    bot.say(instigator + ", It looks like " + target + " has no " +  commandortarget + ".", instigator)
            
        ## Stats
        elif commandortarget == 'stats':
            target = get_trigger_arg(triggerargsarray, 2) or instigator
            if target.lower() not in allusersinroomarray:
                bot.notice(instigator + ", It looks like " + targettext + " is either not here, or not a valid person.", instigator)
            elif target.lower() not in dueloptedinarray:
                bot.notice(instigator + ", It looks like " + target + " has duels off.", instigator)
            else:
                for x in challengestatsarray:
                    if x in statsbypassarray:
                        scriptdef = str('get_' + x + '(bot,target)')
                        gethowmany = eval(scriptdef)
                    else:
                        gethowmany = get_database_value(bot, target, x)
                    if gethowmany:
                        if x == 'winlossratio':
                            gethowmany = format(gethowmany, '.3f')
                        addstat = str(' ' + str(x) + "=" + str(gethowmany))
                        stats = str(stats + addstat)
                if stats != '':
                    pepper = get_pepper(bot, target)
                    targetname = str("(" + str(pepper) + ") " + target)
                    stats = str(targetname + "'s " + commandortarget + ":" + stats)
                    bot.say(stats)
                else:
                    bot.say(instigator + ", It looks like " + target + " has no " +  commandortarget + ".", instigator)

        ## Leaderboard
        elif commandortarget == 'leaderboard':
            for u in dueloptedinarray:
                winlossratio = get_winlossratio(bot,u)
                if winlossratio > currentwlrleadernumber:
                    currentwlrleader = u
                    currentwlrleadernumber = winlossratio
                kills = get_database_value(bot, u, 'kills')
                if int(kills) > int(currentkillsleadernumber):
                    currentkillsleader = u
                    currentkillsleadernumber = int(kills)
                respawns = get_database_value(bot, u, 'respawns')
                if int(respawns) > int(currentrespawnsleadernumber):
                    currentrespawnsleader = u
                    currentrespawnsleadernumber = int(respawns)
                health = get_database_value(bot, u, 'health')
                if int(health) < int(currenthealthleadernumber) and int(health) != 0:
                    currenthealthleader = u
                    currenthealthleadernumber = int(health)
                streaks = get_database_value(bot, u, 'bestwinstreak')
                if int(streaks) > int(currentstreaksleadernumber):
                    currentstreaksleader = u
                    currentstreaksleadernumber = int(streaks)
            if currentwlrleadernumber > 0:
                currentwlrleadernumber = format(currentwlrleadernumber, '.3f')
                leaderboardscript = str(leaderboardscript + "Wins/Losses: " + currentwlrleader + " at " + str(currentwlrleadernumber) + ".     ")
            if currentkillsleadernumber > 0:
                leaderboardscript = str(leaderboardscript + "Top Killer: " + currentkillsleader + " with " + str(currentkillsleadernumber) + " kills.     ")
            if currentrespawnsleadernumber > 0:
                leaderboardscript = str(leaderboardscript + "Top Killed: " + currentrespawnsleader + " with " + str(currentrespawnsleadernumber) + " respawns.     ")
            if currenthealthleadernumber > 0:
                leaderboardscript = str(leaderboardscript + "Closest To Death: " + currenthealthleader + " with " + str(currenthealthleadernumber) + " health.     ")
            if currentstreaksleadernumber > 0:
                leaderboardscript = str(leaderboardscript + "Best Win Streak: " + currentstreaksleader + " with " + str(currentstreaksleadernumber) + ".     ")
            if leaderboardscript == '':
                leaderboardscript = str("Leaderboard appears to be empty")
            bot.say(leaderboardscript)

        ## Loot Items 
        elif commandortarget == 'loot':
            lootcommand = get_trigger_arg(triggerargsarray, 2)
            lootitem = get_trigger_arg(triggerargsarray, 3)
            lootitemb = get_trigger_arg(triggerargsarray, 4)
            lootitemc = get_trigger_arg(triggerargsarray, 5)
            gethowmanylootitem = get_database_value(bot, instigator, lootitem)
            if lootcommand not in transactiontypesarray:
                bot.notice(instigator + ", Do you want to buy, sell, trade, or use?", instigator)
            elif not lootitem:
                bot.notice(instigator + ", What do you want to " + str(lootcommand) + "?", instigator)
            elif lootitem not in lootitemsarray:
                bot.notice(instigator + ", Invalid loot item.", instigator)
            elif lootcommand == 'use':
                if lootitemb.isdigit():
                    quantity = int(lootitemb)
                    target = instigator
                elif lootitemb == 'all':
                    target = instigator
                    quantity = gethowmanylootitem
                elif not lootitemb:
                    quantity = 1
                    target = instigator
                else:
                    target = lootitemb
                    if not lootitemc:
                        quantity = 1
                    elif lootitemc == 'all':
                        quantity = gethowmanylootitem
                    else:
                        quantity = int(lootitemc)
                if gethowmanylootitem < quantity:
                    bot.notice(instigator + ", You do not have enough " +  lootitem + " to use this command!", instigator)
                elif target.lower() not in allusersinroomarray:
                    bot.notice(instigator + ", It looks like " + targettext + " is either not here, or not a valid person.", instigator)
                elif target.lower() not in dueloptedinarray:
                    bot.notice(instigator + ", It looks like " + target + " has duels off.", instigator)
                else:   
                    if int(quantity) == 1:
                        saymsg = 'true'
                        use_lootitem(bot, instigator, target, inchannel, lootitem, saymsg)
                    elif lootitem == 'mysterypotion' and int(quantity) > 1 and inchannel.startswith("#"):
                        bot.notice(instigator + ", Multiple mysterypotions must be used in privmsg.", instigator)
                    else:
                        saymsg = 'false'
                        if lootitem == 'mysterypotion' or not inchannel.startswith("#"):
                            saymsg = 'true'
                        while int(quantity) > 0:
                            quantity = int(quantity) - 1
                            use_lootitem(bot, instigator, target, inchannel, lootitem, saymsg)
                        bot.notice(instigator + ", " + str(lootcommand) + " Completed.", instigator)
            elif lootcommand == 'trade':
                quantity = lootitemc
                if not quantity:
                    quantity = 1
                if yourclass == 'scavenger':
                    quantitymath = 2 * int(quantity)
                else:
                    quantitymath = 3 * int(quantity)
                if lootitemb not in lootitemsarray:
                    bot.notice(instigator + ", You can't trade for the same type of potion.", instigator)
                elif lootitemb not in lootitemsarray:
                    bot.notice(instigator + ", Invalid loot item.", instigator)
                elif lootitemb == lootitem:
                    bot.notice(instigator + ", You can't trade for the same type of potion.", instigator)
                elif gethowmanylootitem < quantitymath:
                    bot.notice(instigator + ", You don't have enough of this item to trade.", instigator)
                else:
                    while int(quantity) > 0:
                        quantity = int(quantity) - 1
                        if yourclass == 'scavenger':
                            cost = -2
                        else:
                            cost = -3
                        reward = 1
                        itemtoexchange = lootitem
                        itemexchanged = lootitemb
                        adjust_database_value(bot, instigator, itemtoexchange, cost)
                        adjust_database_value(bot, instigator, itemexchanged, reward)
                    bot.notice(instigator + ", " + str(lootcommand) + " Completed.", instigator)
            elif lootcommand == 'buy':
                quantity = lootitemb
                if not quantity:
                    quantity = 1
                elif quantity == 'all':
                    quantity = 99999999999999999
                if yourclass == 'scavenger':
                    coinsrequired = 90 * int(quantity)
                else:
                    coinsrequired = 100 * int(quantity)
                if instigatorcoins < coinsrequired:
                    bot.notice(instigator + ", You do not have enough coins for this action.", instigator)
                else:
                    while int(quantity) > 0:
                        quantity = int(quantity) - 1
                        if yourclass == 'scavenger':
                            cost = -90
                        else:
                            cost = -100
                        reward = 1
                        itemtoexchange = 'coins'
                        itemexchanged = lootitem
                        adjust_database_value(bot, instigator, itemtoexchange, cost)
                        adjust_database_value(bot, instigator, itemexchanged, reward)
                    bot.notice(instigator + ", " + str(lootcommand) + " Completed.", instigator)
            elif lootcommand == 'sell':
                quantity = lootitemb
                if not quantity:
                    quantity = 1
                elif quantity == 'all':
                    quantity = gethowmanylootitem
                if int(quantity) > gethowmanylootitem:
                    bot.notice(instigator + ", You do not have enough " + lootitem + " for this action.", instigator)
                else:
                    while int(quantity) > 0:
                        quantity = int(quantity) - 1
                        cost = -1
                        if yourclass == 'scavenger':
                            reward = 30
                        else:
                            reward = 25
                        itemtoexchange = lootitem
                        itemexchanged = 'coins'
                        adjust_database_value(bot, instigator, itemtoexchange, cost)
                        adjust_database_value(bot, instigator, itemexchanged, reward)
                    bot.notice(instigator + ", " + str(lootcommand) + " Completed.", instigator)

        ## Konami
        elif commandortarget == 'upupdowndownleftrightleftrightba':
            konami = get_database_value(bot, target, 'konami')
            if not konami:
                set_database_value(bot, instigator, 'konami', 1)
                bot.notice(instigator + " you have found the cheatcode easter egg!!!", instigator)
                damage = 600
                adjust_database_value(bot, target, 'health', damage)
            else:
                bot.notice(instigator + " you can only cheat once.", instigator)
                
        ## Weaponslocker
        elif commandortarget == 'weaponslocker':
            target = get_trigger_arg(triggerargsarray, 2) or instigator
            validdirectionarray = ['inv','add','del','reset']
            if target in validdirectionarray:
                target = instigator
                adjustmentdirection = get_trigger_arg(triggerargsarray, 2)
                weaponchange = get_trigger_arg(triggerargsarray, '3+')
            else:
                adjustmentdirection = get_trigger_arg(triggerargsarray, 3)
                weaponchange = get_trigger_arg(triggerargsarray, '4+')
            weaponslist = get_database_value(bot, target, 'weaponslocker') or []
            if not adjustmentdirection:
                bot.say('Use .duel weaponslocker add/del to adjust Locker Inventory.')
            elif adjustmentdirection == 'inv' and not inchannel.startswith("#"):
                bot.say("Inventory can only be viewed in privmsg.")
            elif adjustmentdirection == 'inv' and inchannel.startswith("#"):
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
                    bot.say('There doesnt appear to be anything in the weapons locker! Use .duel weaponslocker add/del to adjust Locker Inventory.')
            elif target != instigator and not trigger.admin:
                bot.say("You may not adjust somebody elses locker.")
            elif adjustmentdirection == 'reset':
                set_database_value(bot, target, 'weaponslocker', '')
                bot.say('Locker Reset.')
            else:
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
                        adjust_database_array(bot, target, weaponchange, 'weaponslocker', adjustmentdirection)
                    message = str(weaponchange + " is " + weaponlockerstatus + " in weapons locker.")
                    bot.say(message)
        
        ## Magic Attack
        elif commandortarget == 'magic':
            magicoptions = ['attack','instakill','health','curse','shield']
            magicusage = get_trigger_arg(triggerargsarray, 2)
            if magicusage not in magicoptions:
                bot.say('Magic uses include: attack, instakill, health, curse')
            else:
                target = get_trigger_arg(triggerargsarray, 3) or instigator
                targetcurse = get_curse_check(bot, target)
                targetshield = get_shield_check(bot, target)
                mana = get_database_value(bot, instigator, 'mana')
                if magicusage == 'attack':
                    manarequired = 250
                    damage = -200
                elif magicusage == 'shield':
                    manarequired = 500
                    damage = 80
                elif magicusage == 'curse':
                    manarequired = 500
                    damage = -80
                elif magicusage == 'health':
                    manarequired = 200
                    damage = 200
                elif magicusage == 'instakill':
                    targethealthstart = get_database_value(bot, target, 'health')
                    targethealthstart = int(targethealthstart)
                    if int(targethealthstart) < 200:
                        manarequired = 200
                    else:
                        manarequired = targethealthstart / 200
                        manarequired = manarequired * 250
                    damage = -abs(targethealthstart)
                damagetext = abs(damage)
                yourclass = get_database_value(bot, instigator, 'class') or 'notclassy'
                if yourclass == 'mage':
                    manarequired = manarequired * .9
                if not mana:
                    bot.notice(instigator + " you don't have any mana.", instigator)
                elif int(manarequired) > int(mana):
                    manamath = int(int(manarequired) - int(mana))
                    bot.notice(instigator + " you need " + str(manamath) + " more mana to do this attack.", instigator)
                elif magicusage == 'curse' and targetcurse:
                    bot.notice(instigator + " it looks like " + target + " is already cursed.", instigator)
                elif magicusage == 'shield' and targetshield:
                    bot.notice(instigator + " it looks like " + target + " is already shielded.", instigator)
                else:
                    manarequired = -abs(manarequired)
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
                        elif magicusage == 'curse':
                            curseduration = 4
                            magicsay = str(instigator + " uses magic on " + target + ", dealing " + str(damagetext) + " damage AND forces " + target + " to lose the next " + str(curseduration) + " duels.")
                            magicnotice = str(instigator + " uses magic on " + target + ", dealing " + str(damagetext) + " damage AND forces " + target + " to lose the next " + str(curseduration) + " duels.")
                            set_database_value(bot, target, 'curse', curseduration)
                        elif magicusage == 'shield':
                            shieldduration = 4
                            magicsay = str(instigator + " uses magic on " + target + ", restoring " + str(damagetext) + " health AND allows " + target + " to take no damage for the next " + str(shieldduration) + " duels.")
                            magicnotice = str(instigator + " uses magic on " + target + ", restoring " + str(damagetext) + " health AND allows " + target + " to take no damage for the next " + str(shieldduration) + " duels.")
                            set_database_value(bot, target, 'shield', shieldduration)
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
            
        ## If not a command above, invalid
        else:
            bot.notice(instigator + ", It looks like that is either not here, or not a valid person.", instigator)
    
    ## warning if user doesn't have duels enabled
    elif commandortarget.lower() not in dueloptedinarray:
        bot.notice(instigator + ", It looks like " + target + " has duels off.", instigator)
      
    else:
        OSDTYPE = 'say'
        target = get_trigger_arg(triggerargsarray, 1)
        dowedisplay = 1
        executedueling = mustpassthesetoduel(bot, trigger, instigator, target, inchannel, channel, dowedisplay)
        if executedueling:
            return getreadytorumble(bot, trigger, instigator, target, OSDTYPE, channel, fullcommandused, now, triggerargsarray)
    
    ## bot does not need stats or backpack items
    refreshbot(bot)
        
def getreadytorumble(bot, trigger, instigator, target, OSDTYPE, channel, fullcommandused, now, triggerargsarray):
    
    ## Update Time Of Combat
    set_database_value(bot, instigator, 'timeout', now)
    set_database_value(bot, target, 'timeout', now)
    set_database_value(bot, channel, 'timeout', now)
    
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

    ## Manual weapon
    weapon = get_trigger_arg(triggerargsarray, '2+')
    if not weapon:
        manualweapon = 'false'
    else:
        manualweapon = 'true'
        if weapon == 'all':
            weapon = getallchanweaponsrandom(bot, channel)
        elif weapon == 'target':
            weapon = weaponofchoice(bot, target)
            weapon = str(target + "'s " + weapon)
        
    ## Select Winner
    winner, loser = getwinner(bot, instigator, target, manualweapon)
    
    ## Damage Done (random)
    damage = damagedone(bot, winner, loser)
    
    ## Streaks A
    winner_loss_streak, loser_win_streak = get_streaktexta(bot, winner, loser)
    
    ## Weapon Select
    if manualweapon == 'false' or winner == target:
        if winner == bot.nick:
            weapon = ''
        else:
            weapon = weaponofchoice(bot, winner)
    weapon = weaponformatter(bot, weapon)
    if weapon != '':
        weapon = str(" " + weapon)
        
    ## Update Wins and Losses
    if instigator != target:
        adjust_database_value(bot, winner, 'wins', defaultadjust)
        adjust_database_value(bot, loser, 'losses', defaultadjust)
        set_current_streaks(bot, winner, 'win')
        set_current_streaks(bot, loser, 'loss')
            
    ## Update XP points
    yourclasswinner = get_database_value(bot, winner, 'class') or 'notclassy'
    if yourclasswinner == 'ranger':
        XPearnedwinner = '7'
    else:
        XPearnedwinner = '5'
    yourclassloser = get_database_value(bot, loser, 'class') or 'notclassy'
    if yourclassloser == 'ranger':
        XPearnedloser = '5'
    else:
        XPearnedloser = '3'
    if instigator != target:
        adjust_database_value(bot, winner, 'xp', XPearnedwinner)
        adjust_database_value(bot, loser, 'xp', XPearnedloser)
                
    ## Update last fought
    if instigator != target:
        set_database_value(bot, instigator, 'lastfought', target)
        set_database_value(bot, target, 'lastfought', instigator)
    
    ## Same person can't instigate twice in a row
    set_database_value(bot, channel, 'lastinstigator', instigator)
            
    ## Update Health Of Loser, respawn, allow winner to loot
    yourclass = get_database_value(bot, loser, 'class') or 'notclassy'
    if yourclass == 'rogue':
        if instigator == target or target == bot.nick:
            damage = 0
    adjust_database_value(bot, loser, 'health', damage)
    damage = abs(damage)
    currenthealth = get_database_value(bot, loser, 'health')
    if currenthealth <= 0:
        whokilledwhom(bot, winner, loser)
        if instigator == target:
            loser = targetname
        winnermsg = str(winner + ' killed ' + loser + weapon + ' forcing a respawn!!')
    else:
        if instigator == target:
            loser = targetname
        winnermsg = str(winner + " hits " + loser + weapon + ', dealing ' + str(damage) + ' damage.')
        
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
    randominventoryfind = randominventory(bot, instigator)
    if randominventoryfind == 'true' and target != bot.nick and instigator != target:
        loot = determineloottype(bot, winner)
        loot_text = get_lootitem_text(bot, winner, loot)
        lootwinnermsg = str(instigator + ' found a ' + str(loot) + ' ' + str(loot_text))
        targetclass = get_database_value(bot, target, 'class') or 'notclassy'
        barbarianstealroll = randint(0, 100)
        if winner != target and targetclass == 'barbarian' and barbarianstealroll >= 50:
            lootwinnermsgb = str(target + " steals the " + str(loot))
            adjust_database_value(bot, target, loot, defaultadjust)
        elif winner == target:
            lootwinnermsgb = str(winner + " gains the " + str(loot))
            adjust_database_value(bot, winner, loot, defaultadjust)
        else:
            adjust_database_value(bot, winner, loot, defaultadjust)
    
    # Streaks B
    if instigator != target:
        streaktext = get_streaktext(bot, winner, loser, winner_loss_streak, loser_win_streak) or ''
        if streaktext != '':
            streaktext = str(str(streaktext) + "       ")
    else:
        streaktext = ''
    
    ## On Screen Text
    if OSDTYPE == 'say':
        bot.say(str(announcecombatmsg) + "       " + str(lootwinnermsg))
        bot.say(str(winnermsg)+ "       " + str(lootwinnermsgb))
        if instigatorpeppernow != instigatorpepperstart or targetpeppernow != targetpepperstart or streaktext:
            bot.say(str(streaktext) + str(pepperstatuschangemsg))
    elif OSDTYPE == 'notice':
        bot.notice(str(announcecombatmsg) + "       " + str(lootwinnermsg), winner)
        bot.notice(str(announcecombatmsg) + "       " + str(lootwinnermsg), loser)
        bot.notice(str(winnermsg)+ "       " + str(lootwinnermsgb), winner)
        bot.notice(str(winnermsg)+ "       " + str(lootwinnermsgb), loser)
        if instigatorpeppernow != instigatorpepperstart or targetpeppernow != targetpepperstart or streaktext:
            bot.notice(str(streaktext) + str(pepperstatuschangemsg), winner)
            bot.notice(str(streaktext) + str(pepperstatuschangemsg), loser)
    else:
        bot.say('Looks Like Something went wrong!')
        
        
## 30 minute automation
# health regen
# mysterypotion
# coins
# reset last instigator
@sopel.module.interval(1800)
def healthregen(bot):
    
    ## bot does not need stats or backpack items
    for x in challengestatsadminarray:
        statset = x
        if statset != 'disenable':
            set_database_value(bot, bot.nick, x, '')
    
    ## Clear Last Instigator
    set_database_value(bot, channel, 'lastinstigator', '')
    
    ## Who gets to win a mysterypotion?
    randomtargetarray = []
    lasttimedlootwinner = get_database_value(bot, channel, 'lasttimedlootwinner')
    if not lasttimedlootwinner:
        lasttimedlootwinner = bot.nick
    for channel in bot.channels:
        for u in bot.privileges[channel.lower()]:
            target = u
            targetdisenable = get_database_value(bot, target, 'disenable')
            if targetdisenable and target != lasttimedlootwinner and target != bot.nick:
                ## award 10 coins to everyone
                adjust_database_value(bot, target, 'coins', 10)
                
                ## mages regen mana
                yourclass = get_database_value(bot, target, 'class') or 'notclassy'
                if yourclass == 'mage':
                    mana = get_database_value(bot, target, 'mana')
                    if int(mana) < 1000:
                        adjust_database_value(bot, target, 'mana', '50')
                
                health = get_database_value(bot, target, 'health')
                if int(health) < 500:
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
            set_database_value(bot, channel, 'lasttimedlootwinner', target)
            
        
## Functions######################################################################################################################

######################
## Criteria to duel ##
######################

def mustpassthesetoduel(bot, trigger, instigator, target, inchannel, channel, dowedisplay):
    executedueling = 0
    instigatorlastfought = get_database_value(bot, instigator, 'lastfought') or ''
    instigatordisenable = get_database_value(bot, instigator, 'disenable') or ''
    targetdisenable = get_database_value(bot, target, 'disenable') or ''
    instigatortime = get_timesince_duels(bot, instigator, 'timeout') or ''
    targettime = get_timesince_duels(bot, target, 'timeout') or ''
    channeltime = get_timesince_duels(bot, channel, 'timeout') or ''
    channellastinstigator = get_database_value(bot, channel, 'lastinstigator') or ''
    if not channellastinstigator:
        channellastinstigator = bot.nick
    
    if not inchannel.startswith("#"):
        displaymsg = str(instigator + " Duels must be in channel.")
    elif target == bot.nick and not targetdisenable:
        displaymsg = str(instigator + " I refuse to fight a biological entity!")
    elif instigator == channellastinstigator and not bot.nick.endswith('dev'):
        displaymsg = str(instigator + ', You may not instigate fights twice in a row within a half hour.')
    elif target == instigatorlastfought and not bot.nick.endswith('dev'):
        displaymsg = str(instigator + ', You may not fight the same person twice in a row.')
    elif not instigatordisenable:
        displaymsg = str(instigator + ", It looks like you have disabled Challenges. Run .challenge on to re-enable.")
    elif not targetdisenable:
        displaymsg = str(instigator + ', It looks like ' + target + ' has disabled Challenges.')
    elif instigatortime <= USERTIMEOUT and not bot.nick.endswith('dev'):
        displaymsg = str("You can't challenge for %d seconds." % (USERTIMEOUT - instigatortime))
    elif targettime <= USERTIMEOUT and not bot.nick.endswith('dev'):
        displaymsg = str(target + " can't challenge for %d seconds." % (USERTIMEOUT - targettime))
    elif channeltime <= CHANTIMEOUT and not bot.nick.endswith('dev'):
        displaymsg = str(channel + " can't challenge for %d seconds." % (CHANTIMEOUT - channeltime))
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
    yourclass = get_database_value(bot, loser, 'class') or 'notclassy'
    if yourclass != 'ranger':
        for x in lootitemsarray:
            gethowmany = get_database_value(bot, loser, x)
            adjust_database_value(bot, winner, x, gethowmany)
            set_database_value(bot, loser, x, '')

def healthcheck(bot, nick):
    health = get_database_value(bot, nick, 'health')
    if not health and nick != bot.nick:
        set_database_value(bot, nick, 'health', '1000')

def refreshbot(bot):
    set_database_value(bot, bot.nick, 'disenable', '1')
    for x in challengestatsadminarray:
        statset = x
        if statset != 'disenable':
            set_database_value(bot, bot.nick, x, '')
            
##########
## Time ##
##########
    
def get_timesince_duels(bot, nick, databasekey):
    now = time.time()
    last = get_database_value(bot, nick, databasekey)
    return abs(now - int(last))

def get_timeout(bot, nick):
    time_since = get_timesince_duels(bot, nick, 'timeout')
    if time_since < USERTIMEOUT:
        timediff = int(USERTIMEOUT - time_since)
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
    elif nick in botdevteam:
        nickname = str("The Extraordinary " + nickname)
    elif nick in operatorarray:
        nickname = str("The Magnificent " + nickname)
    elif nick in voicearray:
        nickname = str("The Incredible " + nickname)
    elif nick in adminsarray:
        nickname = str("The Spectacular " + nickname)
    else:
        nickname = str(nickname)
        
    ## Pepper Names
    if pepperstart != '':
        nickname = str(nickname + " (" + pepperstart + ")")
    else:
        nickname = str(nickname + " (n00b)")
    
    return nickname, pepperstart
    
#############
## Streaks ##
#############

def set_current_streaks(bot, nick, winlose):
    if winlose == 'win':
        beststreaktype = 'bestwinstreak'
        currentstreaktype = 'currentwinstreak'
        oppositestreaktype = 'currentlosestreak'
    elif winlose == 'loss':
        beststreaktype = 'worstlosestreak'
        currentstreaktype = 'currentlosestreak'
        oppositestreaktype = 'currentwinstreak'
        
    ## Update Current streak
    adjust_database_value(bot, nick, currentstreaktype, defaultadjust)
    set_database_value(bot, nick, 'currentstreaktype', winlose)
    
    ## Update Best Streak
    beststreak = get_database_value(bot, nick, beststreaktype) or 0
    currentstreak = get_database_value(bot, nick, currentstreaktype) or 0
    if int(currentstreak) > int(beststreak):
        set_database_value(bot, nick, beststreaktype, int(currentstreak))
    
    ## Clear current opposite streak
    set_database_value(bot, nick, oppositestreaktype, '')
    
    
def get_currentstreak(bot, nick):
    streaks = ''
    for x in streaksarray:
        streak = get_database_value(bot, nick, x) or 0
        if streak:
            addstreak = str(str(x) + " = " + str(streak))
            if streaks != '':
                streaks = str(str(streaks) + str(addstreak))
            else:
                streaks = str(str(streaks) + ' ' + str(addstreak))
    return streaks
    
def get_streaktexta(bot, winner, loser):
    winner_loss_streak = get_database_value(bot, winner, 'currentlosestreak') or 0
    loser_win_streak = get_database_value(bot, loser, 'currentwinstreak') or 0
    return winner_loss_streak, loser_win_streak
    
def get_streaktext(bot, winner, loser, winner_loss_streak, loser_win_streak):
    win_streak = get_database_value(bot, winner, 'currentwinstreak') or 0
    streak = ' (Streak: %d)' % win_streak if win_streak > 1 else ''
    broken_streak = ', recovering from a streak of %d losses' % winner_loss_streak if winner_loss_streak > 1 else ''
    broken_streak += ', ending %s\'s streak of %d wins' % (loser, loser_win_streak) if loser_win_streak > 1 else ''
    if broken_streak:
        streaktext = str("%s wins%s!%s" % (winner, broken_streak, streak))
    else:
        streaktext = ''
    return streaktext
    
###############
## Inventory ##
###############

def get_backpackitems(bot, target):
    totalbackpack = 0
    for x in lootitemsarray:
        gethowmany = get_database_value(bot, target, x)
        totalbackpack = int(int(totalbackpack) + int(gethowmany))
    return totalbackpack

def randominventory(bot, instigator):
    yourclass = get_database_value(bot, instigator, 'class') or 'notclassy'
    if yourclass == 'scavenger':
        randomfindchance = randint(40, 120)
    else:
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
        loot_text = ': worth up to ' + str(USERTIMEOUT) + ' seconds of timeout.'
    elif loottype == 'mysterypotion':
        loot_text = ': With unknown effects!'
    else:
        loot_text = ''
    if loot_text != '':
        loot_text = str(loot_text + " Use .challenge loot use " + str(loottype) + " to consume.")
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
        yourclass = get_database_value(bot, target, 'class') or 'notclassy'
        if yourclass != 'rogue':
            adjust_database_value(bot, target, 'health', '-50')
    elif loottype == 'manapotion':
        adjust_database_value(bot, target, 'mana', '100')
    elif loottype == 'timepotion':
        channellastinstigator = get_database_value(bot, channel, 'lastinstigator')
        if not channellastinstigator:
            channellastinstigator = bot.nick
        if channellastinstigator == target:
            set_database_value(bot, channel, 'lastinstigator', '')
        set_database_value(bot, target, 'timeout', '')
        set_database_value(bot, channel, 'timeout', '')
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
            lootusemsg = str("just " + str(nullloot) + ' after all.')
        mainlootusemessage = str(mainlootusemessage + ' It was ' + str(lootusemsg))
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
def getallchanweaponsrandom(bot, channel):
    allchanweaponsarray = []
    for u in bot.channels[channel].users:
        weaponslist = get_database_value(bot, u, 'weaponslocker') or []
        if weaponslist != []:
            for x in weaponslist:
                allchanweaponsarray.append(x)
    if allchanweaponsarray == []:
        weapon = "fist"
    else:
        weaponselected = random.randint(0,len(allchanweaponsarray) - 1)
        weapon = str(allchanweaponsarray [weaponselected])
    return weapon
        
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
    elif weapon.lower().startswith('with'):
        weapon = str(weapon)
    else:
        weapon = str('with a ' + weapon)
    return weapon

#################
## Damage Done ##
#################

def damagedone(bot, winner, loser):
    shieldwinner = get_shield_check(bot, winner)
    shieldloser = get_shield_check(bot, loser)
    yourclass = get_database_value(bot, winner, 'class') or 'notclassy'
    if winner == bot.nick:
        rando = 150
    elif yourclass == 'barbarian':
        rando = randint(40, 120)
    else:
        rando = randint(0, 120)
    if shieldloser:
        damage = 0
    else:
        damage = -abs(rando)
    return damage

##################
## Pepper level ##
##################

def get_pepper(bot, nick):
    xp = get_database_value(bot, nick, 'xp')
    nickcurse = get_database_value(bot, nick, 'curse')
    if nick == bot.nick:
        pepper = 'Dragon Breath Chilli'
    elif nickcurse:
        pepper = 'Cursed'
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
    
    ## each person gets one diceroll
    instigatorfight = 1
    targetfight = 1
    
    instigatoryourclass = get_database_value(bot, instigator, 'class') or ''
    if instigatoryourclass == 'rogue':
        instigatorfight = instigatorfight + 1
    targetyourclass = get_database_value(bot, instigator, 'class') or ''
    if targetyourclass == 'rogue':
        targetfight = targetfight + 1
    
    ## Random Number
    flip = randint(0, 1)
    if flip == 0:
        instigatorfight = instigatorfight + 1
    else:
        targetfight = targetfight + 1
    
    # Most Health Extra roll
    instigatorhealth = get_database_value(bot, instigator, 'health')
    targethealth = get_database_value(bot, target, 'health')
    if int(instigatorhealth) > int(targethealth):
        instigatorfight = instigatorfight + 1
    elif int(instigatorhealth) < int(targethealth):
        targetfight = targetfight + 1
    
    # Most XP gets an extra roll
    instigatorxp = get_database_value(bot, instigator, 'xp')
    targetxp = get_database_value(bot, target, 'xp')
    if int(instigatorxp) > int(targetxp):
        instigatorfight = instigatorfight + 1
    elif int(instigatorxp) < int(targetxp):
        targetfight = targetfight + 1
    
    ## More Kills Gets an extra roll
    instigatorkills = get_database_value(bot, instigator, 'kills')
    targetkills = get_database_value(bot, target, 'kills')
    if int(instigatorkills) > int(targetkills):
        instigatorfight = instigatorfight + 1
    elif int(instigatorkills) < int(targetkills):
        targetfight = targetfight + 1
        
    ## Least Respawns Gets an extra roll
    instigatorrespawns = get_database_value(bot, instigator, 'respawns')
    targetrespawns = get_database_value(bot, target, 'respawns')
    if int(instigatorrespawns) < int(targetrespawns):
        instigatorfight = instigatorfight + 1
    elif int(instigatorrespawns) > int(targetrespawns):
        targetfight = targetfight + 1
    
    # extra roll for using the weaponslocker or manual weapon usage
    instigatorweaponslist = get_database_value(bot, instigator, 'weaponslocker') or []
    targetweaponslist = get_database_value(bot, target, 'weaponslocker') or []
    if instigatorweaponslist != [] or manualweapon == 'true':
        instigatorfight = instigatorfight + 1
    if targetweaponslist != []:
        targetfight = targetfight + 1
    
    ## Dice Roll (instigator d20, target d19)
    instigatorfightarray = []
    targetfightarray = []
    while int(instigatorfight) > 0:
        if targetyourclass == 'rogue':
            instigatorfightroll = randint(10, 20)
        else:
            instigatorfightroll = diceroll(20)
        instigatorfightarray.append(instigatorfightroll)
        instigatorfight = int(instigatorfight) - 1
    instigatorfight = max(instigatorfightarray)
    while int(targetfight) > 0:
        if targetyourclass == 'rogue':
            targetfightroll = randint(10, 22)
        else:
            targetfightroll = diceroll(19)
        targetfightarray.append(targetfightroll)
        targetfight = int(targetfight) - 1
    targetfight = max(targetfightarray)

    ## check for curses
    if instigator != target and instigator != bot.nick:
        instigatorcurse = get_curse_check(bot, instigator)
        if instigatorcurse:
            instigatorfight = 0
        targetcurse = get_curse_check(bot, target)
        if targetcurse:
            targetfight = 0

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
    if target == bot.nick:
        winner = bot.nick
        loser = instigator
    elif winner == instigator:
        loser = target
    else:
        loser = instigator
    return winner, loser

############
## cursed ##
############

def get_curse_check(bot, nick):
    adjustment = -1
    cursed = 0
    nickcurse = get_database_value(bot, nick, 'curse')
    if nickcurse:
        adjust_database_value(bot, nick, 'curse', adjustment)
        cursed = 1
    return cursed

############
## shield ##
############

def get_shield_check(bot, nick):
    adjustment = -1
    shield = 0
    nickshield = get_database_value(bot, nick, 'shield')
    if nickshield:
        adjust_database_value(bot, nick, 'shield', adjustment)
        shield = 1
    return shield
    
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

##########
## ARGS ##
##########

def create_args_array(fullstring):
    triggerargsarray = []
    if fullstring:
        for word in fullstring.split():
            triggerargsarray.append(word)
    return triggerargsarray

def get_trigger_arg(triggerargsarray, number):
    totalarray = len(triggerargsarray)
    totalarray = totalarray + 1
    triggerarg = ''
    if "^" in str(number) or number == 0 or str(number).endswith("+") or str(number).endswith("-") or str(number).endswith("<") or str(number).endswith(">"):
        if str(number).endswith("+"):
            rangea = re.sub(r"\+", '', str(number))
            rangea = int(rangea)
            rangeb = totalarray
        elif str(number).endswith("-"):
            rangea = 1
            rangeb = re.sub(r"-", '', str(number))
            rangeb = int(rangeb) + 1
        elif str(number).endswith(">"):
            rangea = re.sub(r">", '', str(number))
            rangea = int(rangea) + 1
            rangeb = totalarray
        elif str(number).endswith("<"):
            rangea = 1
            rangeb = re.sub(r"<", '', str(number))
            rangeb = int(rangeb)
        elif "^" in str(number):
            rangea = number.split("^", 1)[0]
            rangeb = number.split("^", 1)[1]
            rangea = int(rangea)
            rangeb = int(rangeb) + 1
        elif number == 0:
            rangea = 1
            rangeb = totalarray
        if rangea <= totalarray:
            for i in range(rangea,rangeb):
                arg = get_trigger_arg(triggerargsarray, i)
                if triggerarg != '':
                    triggerarg = str(triggerarg + " " + arg)
                else:
                    triggerarg = str(arg)
    elif number == 'last':
        totalarray = totalarray -2
        triggerarg = str(triggerargsarray[totalarray])
    elif str(number).endswith("!"):
        number = re.sub(r"!", '', str(number))
        for i in range(1,totalarray):
            if int(i) != int(number):
                arg = get_trigger_arg(triggerargsarray, i)
                if triggerarg != '':
                    triggerarg = str(triggerarg + " " + arg)
                else:
                    triggerarg = str(arg)
    else:
        number = int(number) - 1
        try:
            triggerarg = triggerargsarray[number]
        except IndexError:
            triggerarg = ''
    return triggerarg
