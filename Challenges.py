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
devbot = 'dev' ## If using a development bot and want to bypass commands, this is what the bots name ends in
stockhealth = 1000 ## default health for new players and respawns
changeclasscost = 100 ## ## how many coins to change class
botonoffstatus = 1 ## does the bot paricipate in duels

## Half hour timer
halfhourcoinaward = 10
magemanaregen = 50
healthregen = 50
magemanaregenmax = 500
healthregenmax = 500

## Potion Potency
healthpotionworthbarbarian = 125 ## health potion worth for barbarians
healthpotionworth = 100 ## normal health potion worth
poisonpotionworth = -50 ## poisonpotion damage
manapotionworthmage = 125 ## manapotion worth for mages
manapotionworth = 100 ##normal mana potion worth

## Buy/sell/trade rates
traderatioscavenger = 2 ## scavengers can trade at a 2:1 ratio
traderatio = 3 ## normal trading ratio 3:1
lootbuycostscavenger = 90 ## cost to buy a loot item for scavengers
lootbuycost = 100 ## normal cost to buy a loot item
lootsellrewardscavenger = 30 ## coins rewarded in selling loot for scavengers
lootsellreward = 25 ## normal coins rewarded in selling loot

## Magic usage
magemanamagiccut = .9 ## mages only need 90% of the mana requirements below
manarequiredmagicattack = 250 ## mana required for magic attack
magicattackdamage = -200 ## damage caused by a magic attack
manarequiredmagicshield = 500 ## mana required for magic shield
magicshielddamage = 80 ## damage caused by a magic shield usage
shieldduration = 4 ## how long a shield lasts
manarequiredmagiccurse = 500 ## mana required for magic curse
magiccursedamage = -80 ## damage caused by a magic curse
curseduration = 4 ## how long a curse lasts
manarequiredmagichealth = 200 ## mana required for magic health
magichealthrestore = 200 ## health restored by a magic health

## XP points awarded
XPearnedwinnerranger = 7
XPearnedloserranger = 5
XPearnedwinnerstock = 5
XPearnedloserstock = 3

## other
scavegerfindpercent = 40
barbarianminimumdamge = 40
botdamage = 150

############
## Arrays ##
############

botdevteam = ['deathbybandaid','DoubleD','Mace_Whatdo','dysonparkes','PM','under_score']
lootitemsarray = ['healthpotion','manapotion','poisonpotion','timepotion','mysterypotion']
backpackarray = ['weaponstotal','coins','healthpotion','manapotion','poisonpotion','timepotion','mysterypotion']
transactiontypesarray = ['buy','sell','trade','use']
challengestatsadminarray = ['shield','classtimeout','class','curse','bestwinstreak','worstlosestreak','opttime','coins','wins','losses','health','mana','healthpotion','mysterypotion','timepotion','respawns','xp','kills','timeout','disenable','poisonpotion','manapotion','lastfought','konami']
challengestatsarray = ['class','health','curse','shield','mana','xp','wins','losses','winlossratio','respawns','kills','lastfought','timeout']
classarray = ['barbarian','mage','scavenger','rogue','ranger']
statsadminchangearray = ['set','reset']
statsbypassarray = ['winlossratio','timeout']
             
################################################################################
## Main Operation #### Main Operation #### Main Operation #### Main Operation ##
################################################################################

@sopel.module.commands('challenge','duel')
def execute_main(bot, trigger):
    
    ## Initial ARGS of importance
    triggerargsarray = create_args_array(trigger.group(2))
    fullcommandused = get_trigger_arg(triggerargsarray, 0)
    commandortarget = get_trigger_arg(triggerargsarray, 1)
    dowedisplay = 0
    displaymessage = ''
    
    ## Build User/channel Arrays
    targetarray, targetcantoptarray, canduelarray, classcantchangearray, botownerarray, operatorarray, voicearray, adminsarray, allusersinroomarray, dueloptedinarray, channelarray = [], [], [], [], [], [], [], [], [], [], []
    for c in bot.channels:
        channelarray.append(c)
        inchannel = "#bypass"
        ## All Users in channel
        for u in bot.channels[c.lower()].users:
            allusersinroomarray.append(u)
            ## Users that can opt in/out of duels
            opttime = get_timesince_duels(bot, u, 'opttime')
            if opttime < OPTTIMEOUT and not bot.nick.endswith(devbot):
                targetcantoptarray.append(u)
            # Users with duels enabled
            disenable = get_database_value(bot, u, 'disenable')
            if u != bot.nick and disenable:
                dueloptedinarray.append(u)
            # Target passes all duel checks
            canduel = mustpassthesetoduel(bot, trigger, u, bot.nick, inchannel, c, dowedisplay)
            if canduel and u != bot.nick:
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
            if classtime < CLASSTIMEOUT and not bot.nick.endswith(devbot):
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
    adjust_database_value(bot, instigator, 'usage', 1)
    healthcheck(bot, instigator)
    instigatortime = get_timesince_duels(bot, instigator, 'timeout') or USERTIMEOUT
    instigatorlastfought = get_database_value(bot, instigator, 'lastfought') or instigator
    instigatorcoins = get_database_value(bot, instigator, 'coins') or 0
    instigatorclass = get_database_value(bot, instigator, 'class')

    ## Channel Information
    adjust_database_value(bot, channel, 'usage', 1)
    channeltime = get_timesince_duels(bot, channel, 'timeout') or CHANTIMEOUT
    channellastinstigator = get_database_value(bot, channel, 'lastinstigator') or bot.nick
    lastfullroomassult = get_timesince_duels(bot, channel, 'lastfullroomassult') or ASSAULTTIMEOUT
    lastfullroomassultinstigator = get_database_value(bot, channel, 'lastfullroomassultinstigator') or bot.nick
    
    ## The only commands that should get through if instigator doesn't have duels enabled
    commandbypassarray = ['on','off']
    
    ## If Not a target or a command used
    if not fullcommandused:
        bot.notice(instigator + ", Who did you want to challenge? Online Docs: " + GITWIKIURL, instigator)
    
    ## commands cannot be run if opted out
    elif instigator not in dueloptedinarray and commandortarget not in commandbypassarray:
        bot.notice(instigator + ", It looks like you have duels off.", instigator)
    
    ## Determine if the arg after .duel is a target or a command
    elif commandortarget.lower() not in [x.lower() for x in allusersinroomarray]:
        commandortarget = commandortarget.lower()
                
        ## Docs
        if commandortarget == 'docs' or commandortarget == 'help' or commandortarget == 'help':
            target = get_trigger_arg(triggerargsarray, 2)
            if not target:
                bot.say("Online Docs: " + GITWIKIURL)
            elif target.lower() not in allusersinroomarray:
                bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
            else:
                bot.notice("Online Docs: " + GITWIKIURL, target)
        
        ## On/off
        elif commandortarget == 'on' or commandortarget == 'off':
            disenablevalue = None
            if commandortarget == 'on':
                disenablevalue = 1
            target = get_trigger_arg(triggerargsarray, 2) or instigator
            if target.lower() not in allusersinroomarray and target != 'everyone':
                bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
            elif target != instigator and instigator not in adminsarray:
                bot.notice(instigator + "This is an admin only function.", instigator)
            elif target == 'everyone':
                for u in allusersinroomarray:
                    set_database_value(bot, u, 'disenable', disenablevalue)
                bot.notice(instigator + ", Challenges should now be " +  commandortarget + ' for ' + target + '.', instigator)
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
        
        ## Usage
        elif commandortarget == 'usage':
            target = get_trigger_arg(triggerargsarray, 2) or instigator
            targetname = target
            if target == 'channel':
                target = channel
            totaluses = get_database_value(bot, target, 'usage')
            bot.say(targetname + " has used challenges " + str(totaluses) + " times.")
                
        ## Random Dueling
        elif commandortarget == 'random':
            if canduelarray == []:
                bot.notice(instigator + ", It looks like the random target finder has failed.", instigator)
            else:
                target = get_trigger_arg(canduelarray, 'random')
                OSDTYPE = 'say'
                return getreadytorumble(bot, trigger, instigator, target, OSDTYPE, channel, fullcommandused, now, triggerargsarray)
        
        ## Duel Everyone
        elif commandortarget == 'assault':
            fullchanassaultarray = []
            for x in canduelarray:
                if x != instigator and x != bot.nick:
                    fullchanassaultarray.append(x)
            fullchanassaultarraytotal = len(fullchanassaultarray)
            if lastfullroomassult < ASSAULTTIMEOUT and not bot.nick.endswith(devbot):
                bot.notice(instigator + ", Full Channel Assault can't be used for %d seconds." % (ASSAULTTIMEOUT - lastfullroomassult), instigator)
            elif lastfullroomassultinstigator == instigator and not bot.nick.endswith(devbot):
                bot.notice(instigator + ", You may not instigate a Full Channel Assault twice in a row.", instigator)
            elif instigator not in canduelarray:
                bot.notice(instigator + ", It looks like you can't duel right now.", instigator)
            elif fullchanassaultarray == []:
                bot.notice(instigator + ", It looks like the Full Channel Assault target finder has failed.", instigator)
            else:
                OSDTYPE = 'notice'
                set_database_value(bot, channel, 'lastfullroomassult', now)
                set_database_value(bot, channel, 'lastfullroomassultinstigator', instigator)
                lastfoughtstart = get_database_value(bot, instigator, 'lastfought')
                for u in fullchanassaultarray:
                    if u != instigator and u != bot.nick:
                        targetlastfoughtstart = get_database_value(bot, u, 'lastfought')
                        getreadytorumble(bot, trigger, instigator, u, OSDTYPE, channel, fullcommandused, now, triggerargsarray)
                        fullchanassaultarraytotal = fullchanassaultarraytotal - 1
                        if fullchanassaultarraytotal > 0:
                            bot.notice("  ", instigator)
                            time.sleep(5)
                        set_database_value(bot, u, 'lastfought', targetlastfoughtstart)
                set_database_value(bot, instigator, 'lastfought', lastfoughtstart)
                bot.notice(instigator + ", It looks like the Full Channel Assault has completed.", instigator)

        ## War Room
        elif commandortarget == 'warroom':
            inchannel = "#bypass"
            dowedisplay = 1
            subcommand = get_trigger_arg(triggerargsarray, 2)
            if not subcommand:
                if instigator in canduelarray:
                    bot.notice(instigator + ", It looks like you can challenge.", instigator)
                else:
                    mustpassthesetoduel(bot, trigger, instigator, instigator, inchannel, channel, dowedisplay)
            elif subcommand == 'assault':
                if lastfullroomassultinstigator == instigator and not bot.nick.endswith(devbot):
                    bot.notice(instigator + ", You may not instigate a Full Channel Assault twice in a row.", instigator)
                elif lastfullroomassult < ASSAULTTIMEOUT and not bot.nick.endswith(devbot):
                    bot.notice(instigator + ", Full Channel Assault can't be used for %d seconds." % (ASSAULTTIMEOUT - lastfullroomassult), instigator)
                else:
                    bot.notice(instigator + ", Full Channel Assault can be used.", instigator)
            elif subcommand == 'list':
                displaymessage = get_trigger_arg(canduelarray, "list")
                bot.say(str(displaymessage ))
            elif subcommand.lower() not in allusersinroomarray:
                bot.notice(instigator + ", It looks like " + str(subcommand) + " is either not here, or not a valid person.", instigator)
            else:
                if subcommand in canduelarray:
                    bot.notice(instigator + ", It looks like you can challenge " + subcommand + ".", instigator)
                else:
                    mustpassthesetoduel(bot, trigger, instigator, subcommand, inchannel, channel, dowedisplay)

        ## Stats Admin
        elif commandortarget == 'statsadmin':
            incorrectdisplay = "A correct command use is .duel statsadmin target set/reset stat"
            target = get_trigger_arg(triggerargsarray, 2)
            subcommand = get_trigger_arg(triggerargsarray, 3)
            statset = get_trigger_arg(triggerargsarray, 4)
            newvalue = get_trigger_arg(triggerargsarray, 5) or None
            if not target:
                bot.notice(instigator + ", Target Missing. " + incorrectdisplay, instigator)
            elif target.lower() not in allusersinroomarray and target != 'everyone':
                bot.notice(instigator + ", It looks like " + str(target) + " is either not here, or not a valid person.", instigator)
            elif not subcommand:
                bot.notice(instigator + ", Subcommand Missing. " + incorrectdisplay, instigator)
            elif subcommand not in statsadminchangearray:
                bot.notice(instigator + ", Invalid subcommand. " + incorrectdisplay, instigator)
            elif not statset:
                bot.notice(instigator + ", Stat Missing. " + incorrectdisplay, instigator)
            elif statset not in challengestatsadminarray and statset != 'all':
                bot.notice(instigator + ", Invalid stat. " + incorrectdisplay, instigator)
            elif instigator not in adminsarray:
                bot.notice(instigator + "This is an admin only function.", instigator)
            else:
                if subcommand == 'reset':
                    newvalue = None
                if subcommand == 'set' and newvalue == None:
                    bot.notice(instigator + ", When using set, you must specify a value. " + incorrectdisplay, instigator)
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
            classes = get_trigger_arg(classarray, "list")
            subcommand = get_trigger_arg(triggerargsarray, 2)
            setclass = get_trigger_arg(triggerargsarray, 3)
            if not instigatorclass and not subcommand:
                bot.say("You don't appear to have a class set. Options are : " + classes + ". Run .duel class set    to set your class.")
            elif not subcommand:
                bot.say("Your class is currently set to " + str(instigatorclass) + ". Use .duel class change    to change class. Options are : " + classes + ".")
            elif instigator in classcantchangearray and not bot.nick.endswith(devbot):
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
                bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
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
                    displaymessage = str(displaymessage + "Currently on a " + typeofstreak + " streak of " + str(streak_count) + ".     ")
                if int(best_wins) > 1:
                    displaymessage = str(displaymessage + "Best Win streak= " + str(best_wins) + ".     ")
                if int(worst_losses) > 1:
                    displaymessage = str(displaymessage + "Worst Losing streak= " + str(worst_losses) + ".     ")
                if displaymessage == '':
                    bot.say(target + " has no streaks.")
                else:
                    bot.say(target + "'s streaks: " + displaymessage)
            
        ## Backpack
        elif commandortarget == 'backpack':
            target = get_trigger_arg(triggerargsarray, 2) or instigator
            if target.lower() not in allusersinroomarray:
                bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
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
                        displaymessage = str(displaymessage + addstat)
                if displaymessage != '':
                    displaymessage = str(target + "'s " + commandortarget + ":" + displaymessage)
                    bot.say(displaymessage)
                else:
                    bot.say(instigator + ", It looks like " + target + " has no " +  commandortarget + ".", instigator)
            
        ## Stats
        elif commandortarget == 'stats':
            target = get_trigger_arg(triggerargsarray, 2) or instigator
            if target.lower() not in allusersinroomarray:
                bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
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
                        displaymessage = str(displaymessage + addstat)
                if displaymessage != '':
                    pepper = get_pepper(bot, target)
                    targetname = str("(" + str(pepper) + ") " + target)
                    displaymessage = str(targetname + "'s " + commandortarget + ":" + displaymessage)
                    bot.say(displaymessage)
                else:
                    bot.say(instigator + ", It looks like " + target + " has no " +  commandortarget + ".", instigator)

        ## Leaderboard
        elif commandortarget == 'leaderboard':
            currentwlrleader, currentkillsleader, currentrespawnsleader, currenthealthleader, currentstreaksleader  = '', '', '', '', ''
            currentwlrleadernumber, currentkillsleadernumber, currentrespawnsleadernumber, currentstreaksleadernumber, currentstreaksleadernumber  = 0, 0, 0, 0, 0
            currenthealthleadernumber = 9999999999
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
                displaymessage = str(displaymessage + "Wins/Losses: " + currentwlrleader + " at " + str(currentwlrleadernumber) + ".     ")
            if currentkillsleadernumber > 0:
                displaymessage = str(displaymessage + "Top Killer: " + currentkillsleader + " with " + str(currentkillsleadernumber) + " kills.     ")
            if currentrespawnsleadernumber > 0:
                displaymessage = str(displaymessage + "Top Killed: " + currentrespawnsleader + " with " + str(currentrespawnsleadernumber) + " respawns.     ")
            if currenthealthleadernumber > 0:
                displaymessage = str(displaymessage + "Closest To Death: " + currenthealthleader + " with " + str(currenthealthleadernumber) + " health.     ")
            if currentstreaksleadernumber > 0:
                displaymessage = str(displaymessage + "Best Win Streak: " + currentstreaksleader + " with " + str(currentstreaksleadernumber) + ".     ")
            if displaymessage == '':
                displaymessage = str("Leaderboard appears to be empty")
            bot.say(displaymessage)


        ## Loot Items 
        elif commandortarget == 'loot':
            lootcommand = get_trigger_arg(triggerargsarray, 2)
            lootitem = get_trigger_arg(triggerargsarray, 3)
            lootitemb = get_trigger_arg(triggerargsarray, 4)
            lootitemc = get_trigger_arg(triggerargsarray, 5)
            gethowmanylootitem = get_database_value(bot, instigator, lootitem) or 0
            if not lootcommand:
                bot.notice(instigator + ", Do you want to buy, sell, trade, or use?", instigator)
            elif lootcommand not in transactiontypesarray:
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
                    quantity = int(gethowmanylootitem)
                elif not lootitemb:
                    quantity = 1
                    target = instigator
                else:
                    target = lootitemb
                    if not lootitemc:
                        quantity = 1
                    elif lootitemc == 'all':
                        quantity = int(gethowmanylootitem)
                    else:
                        quantity = int(lootitemc)
                if not gethowmanylootitem:
                    bot.notice(instigator + ", You do not have any " +  lootitem + "!", instigator)
                elif int(gethowmanylootitem) < int(quantity):
                    bot.notice(instigator + ", You do not have enough " +  lootitem + " to use this command!", instigator)
                elif target.lower() not in allusersinroomarray:
                    bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
                elif target == bot.nick:
                  bot.notice(instigator + ", I am immune to " + lootitem, instigator)
                elif target.lower() not in dueloptedinarray:
                    bot.notice(instigator + ", It looks like " + target + " has duels off.", instigator)
                else:
                    lootusedeaths = 0
                    killedmsg = ''
                    targethealth = get_database_value(bot, target, 'health') or 0
                    targetmana = get_database_value(bot, target, 'mana') or 0
                    targetclass = get_database_value(bot, target, 'class') or 'notclassy'
                    if not targethealth:
                        set_database_value(bot, target, 'health', stockhealth)
                        targethealth = get_database_value(bot, target, 'health')
                    uselootarray = []
                    if lootitem == 'mysterypotion':
                        while int(quantity) > 0:
                            quantity = quantity - 1
                            loot = get_trigger_arg(lootitemsarray, 'random')
                            uselootarray.append(loot)
                            adjust_database_value(bot, instigator, lootitem, -1)
                    else:
                        while int(quantity) > 0:
                            quantity = int(quantity) - 1
                            uselootarray.append(lootitem)
                            adjust_database_value(bot, instigator, lootitem, -1)
                    uselootarraytotal = len(uselootarray)
                    if int(uselootarraytotal) == 1 and lootitem != 'mysterypotion':
                        if target == instigator:
                            mainlootusemessage = str(instigator + ' uses ' + lootitem + '.')
                        else:
                            mainlootusemessage = str(instigator + ' uses ' + lootitem + ' on ' + target + ".")
                        if target != instigator:
                            notifytargetmessage = str(instigator + " used a " + lootitem + " on you.")
                    elif int(uselootarraytotal) > 1 and lootitem != 'mysterypotion':
                        if not inchannel.startswith("#"):
                            mainlootusemessage = str(instigator + ", " + str(lootcommand) + " Completed.")
                        elif target == instigator:
                            mainlootusemessage = str(instigator + ' uses ' + str(uselootarraytotal) + " " + lootitem + 's.')
                        else:
                            mainlootusemessage = str(instigator + " used " + str(uselootarraytotal) + " " + lootitem + "s on " + target +".")
                        if target != instigator:
                            notifytargetmessage = str(instigator + " used " + str(uselootarraytotal) + " " + lootitem + "s on you.")
                    else:
                        mainlootusemessage = ''
                        notifytargetmessage = ''
                    for x in uselootarray:
                        lootusemsg = ''
                        if x == 'healthpotion':
                            if targetclass == 'barbarian':
                                adjust_database_value(bot, target, 'health', healthpotionworthbarbarian)
                            else:
                                adjust_database_value(bot, target, 'health', healthpotionworth)
                        elif x == 'poisonpotion':
                            if targetclass != 'rogue':
                                adjust_database_value(bot, target, 'health', poisonpotionworth)
                        elif x == 'manapotion':
                            if targetclass == 'mage':
                                adjust_database_value(bot, target, 'mana', manapotionworthmage)
                            else:
                                adjust_database_value(bot, target, 'mana', manapotionworth)
                        elif x == 'timepotion':
                            channellastinstigator = get_database_value(bot, channel, 'lastinstigator') or bot.nick
                            if channellastinstigator == target:
                                set_database_value(bot, channel, 'lastinstigator', None)
                            set_database_value(bot, target, 'timeout', None)
                            set_database_value(bot, channel, 'timeout', None)
                        else:
                            nulllootitemsarray = ['water','vinegar','mud']
                            nullloot = get_trigger_arg(nulllootitemsarray, 'random')
                            lootusemsg = str("It turned out to be just " + str(nullloot) + ' after all.')
                        targethealth = get_database_value(bot, target, 'health')
                        if targethealth <= 0:
                            lootusedeaths = lootusedeaths + 1
                            whokilledwhom(bot, instigator, target)
                            if lootusedeaths > 1:
                                killedmsg = str("This resulted in " + str(lootusedeaths) +" deaths.")
                            else:
                                killedmsg = "This resulted in death."
                        if lootitem == 'mysterypotion':
                            if lootusemsg == '':
                                lootusemsg = str("It was a " + str(x) + "!")
                            if targethealth <= 0:
                                lootusemsg = str(lootusemsg + " This resulted in death.")
                            if target == instigator:
                                bot.notice(instigator + " used a mysterypotion. " + lootusemsg, instigator)
                            else:
                                bot.notice(instigator + " used a mysterypotion on " + target + ". " + lootusemsg, instigator)
                            if target != instigator:
                                bot.notice(instigator + " used a mysterypotion on you. " + lootusemsg, target)
                    if lootitem != 'mysterypotion':
                        bot.say(mainlootusemessage + " " + killedmsg)
                        if target != instigator and not inchannel.startswith("#"):
                            bot.notice(instigator + " " + notifytargetmessage + " " + lootusemsg, target) 
            elif lootcommand == 'trade':
                quantity = lootitemc
                if not quantity:
                    quantity = 1
                if instigatorclass == 'scavenger':
                    quantitymath = traderatioscavenger * int(quantity)
                else:
                    quantitymath = traderatio * int(quantity)
                if lootitemb not in lootitemsarray:
                    bot.notice(instigator + ", You can't trade for the same type of potion.", instigator)
                elif lootitemb not in lootitemsarray:
                    bot.notice(instigator + ", Invalid loot item.", instigator)
                elif lootitemb == lootitem:
                    bot.notice(instigator + ", You can't trade for the same type of potion.", instigator)
                elif gethowmanylootitem < quantitymath:
                    bot.notice(instigator + ", You don't have enough of this item to trade.", instigator)
                else:
                    while int(quantity) > 1:
                        quantity = int(quantity) - 1
                        if instigatorclass == 'scavenger':
                            cost = traderatioscavenger
                        else:
                            cost = traderatio
                        reward = 1
                        itemtoexchange = lootitem
                        itemexchanged = lootitemb
                        adjust_database_value(bot, instigator, itemtoexchange, -abs(cost))
                        adjust_database_value(bot, instigator, itemexchanged, reward)
                    bot.notice(instigator + ", " + str(lootcommand) + " Completed.", instigator)
            elif lootcommand == 'buy':
                quantity = lootitemb
                if not quantity:
                    quantity = 1
                elif quantity == 'all':
                    quantity = 99999999999999999
                if instigatorclass == 'scavenger':
                    coinsrequired = lootbuycostscavenger * int(quantity)
                else:
                    coinsrequired = lootbuycost * int(quantity)
                if instigatorcoins < coinsrequired:
                    bot.notice(instigator + ", You do not have enough coins for this action.", instigator)
                else:
                    while int(quantity) > 0:
                        quantity = int(quantity) - 1
                        if instigatorclass == 'scavenger':
                            cost = lootbuycostscavenger
                        else:
                            cost = lootbuycost
                        reward = 1
                        itemtoexchange = 'coins'
                        itemexchanged = lootitem
                        adjust_database_value(bot, instigator, itemtoexchange, -abs(cost))
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
                        if instigatorclass == 'scavenger':
                            reward = lootsellrewardscavenger
                        else:
                            reward = lootsellreward
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
                konamiset = 600
                adjust_database_value(bot, target, 'health', konamiset)
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
                bot.notice(instigator + ", Use .duel weaponslocker add/del to adjust Locker Inventory.", instigator)
            elif adjustmentdirection == 'inv' and not inchannel.startswith("#"):
                bot.notice(instigator + ", Inventory can only be viewed in privmsg.", instigator)
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
                    bot.notice(instigator + ", There doesnt appear to be anything in the weapons locker! Use .duel weaponslocker add/del to adjust Locker Inventory.", instigator)
            elif target != instigator and not trigger.admin:
                bot.notice(instigator + ", You may not adjust somebody elses locker.", instigator)
            elif adjustmentdirection == 'reset':
                set_database_value(bot, target, 'weaponslocker', None)
                bot.notice(instigator + ", Locker Reset.", instigator)
            else:
                if not weaponchange:
                    bot.notice(instigator + ", What weapon would you like to add/remove?", instigator)
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
                    bot.notice(instigator + ", " + message, instigator)
        
        ## Magic Attack
        elif commandortarget == 'magic':
            magicoptions = ['attack','instakill','health','curse','shield']
            mana = get_database_value(bot, instigator, 'mana')
            magicusage = get_trigger_arg(triggerargsarray, 2)
            target = get_trigger_arg(triggerargsarray, 3)
            if not target:
                target = instigator
                quantity = 1
            elif target.isdigit():
                quantity = get_trigger_arg(triggerargsarray, 3)
                target = instigator
            else:
                quantity = get_trigger_arg(triggerargsarray, 4)
            if not quantity:
                quantity = 1
            targetcurse = get_curse_check(bot, target)
            targetshield = get_shield_check(bot, target)
            if not magicusage:
                bot.say('Magic uses include: attack, instakill, health, curse, shield')
            elif magicusage not in magicoptions:
                bot.say('Magic uses include: attack, instakill, health, curse, shield')
            elif target.lower() not in allusersinroomarray:
                bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
            elif target == bot.nick:
                bot.notice(instigator + ", I am immune to magic " + magicusage, instigator)
            elif target.lower() not in dueloptedinarray:
                bot.notice(instigator + ", It looks like " + target + " has duels off.", instigator)
            elif not mana:
                bot.notice(instigator + " you don't have any mana.", instigator)
            elif magicusage == 'curse' and targetcurse:
                bot.notice(instigator + " it looks like " + target + " is already cursed.", instigator)
            elif magicusage == 'shield' and targetshield:
                bot.notice(instigator + " it looks like " + target + " is already shielded.", instigator)
            elif magicusage == 'curse' and quantity > 1:
                bot.notice(instigator + " You cannot apply a multi-curse.", instigator)
            elif magicusage == 'shield' and quantity > 1:
                bot.notice(instigator + " You cannot apply a multi-shield.", instigator)
            else:
                if magicusage == 'attack':
                    manarequired = manarequiredmagicattack
                    damage = magicattackdamage
                elif magicusage == 'shield':
                    manarequired = manarequiredmagicshield
                    damage = magicshielddamage
                elif magicusage == 'curse':
                    manarequired = manarequiredmagiccurse
                    damage = magiccursedamage
                elif magicusage == 'health':
                    manarequired = manarequiredmagichealth
                    damage = magichealthrestore
                elif magicusage == 'instakill':
                    targethealthstart = get_database_value(bot, target, 'health')
                    targethealthstart = int(targethealthstart)
                    if int(targethealthstart) < 200:
                        manarequired = manarequiredmagicattack
                    else:
                        manarequired = targethealthstart / 200
                        manarequired = manarequired * manarequiredmagicattack
                    damage = -abs(targethealthstart)
                if instigatorclass == 'mage':
                    manarequired = manarequired * magemanamagiccut
                if magicusage == 'instakill':
                    actualmanarequired = int(manarequired)
                    instaquantity = int(quantity)
                    if int(instaquantity) > 1:
                        instaquantity = int(instaquantity) - 1
                        quantityadjust = stockhealth * int(instaquantity)
                        quantityadjust = quantityadjust / 200
                        quantityadjust = quantityadjust * manarequiredmagicattack
                        actualmanarequired = int(quantityadjust) + int(manarequired)
                else:
                    actualmanarequired = int(manarequired) * int(quantity)
                targethealthstart = get_database_value(bot, target, 'health')
                if int(actualmanarequired) > int(mana):
                    manamath = int(int(actualmanarequired) - int(mana))
                    bot.notice(instigator + " you need " + str(manamath) + " more mana to use magic " + magicusage + ".", instigator)
                else:
                    damagedealt = 0
                    magickilled = ''
                    magicdeaths = 0
                    specialtext = ''
                    damageorhealth = 'dealing'
                    damageorhealthb = 'damage'
                    manarequired = -abs(manarequired)
                    adjust_database_value(bot, instigator, 'mana', manarequired)
                    while int(quantity) > 0:
                        quantity = int(quantity) - 1
                        if magicusage == 'instakill':
                            targethealthcurrent = get_database_value(bot, target, 'health')
                            adjust_database_value(bot, target, 'health', -abs(int(targethealthcurrent)))
                            damagedealt = int(damagedealt) + int(targethealthcurrent)
                        else:
                            adjust_database_value(bot, target, 'health', int(damage))
                            damagedealt = int(damagedealt) + int(abs(damage))
                        targethealth = get_database_value(bot, target, 'health')
                        if int(targethealth) <= 0:
                            magicdeaths = magicdeaths + 1
                            whokilledwhom(bot, instigator, target)
                            if int(magicdeaths) > 1:
                                magickilled = str("This resulted in " + str(magicdeaths) +" deaths.")
                            else:
                                magickilled = "This resulted in death."
                        if magicusage == 'curse':
                            set_database_value(bot, target, 'curse', curseduration)
                            specialtext = str("AND forces " + target + " to lose the next " + str(curseduration) + " duels.")
                        elif magicusage == 'shield':
                            set_database_value(bot, target, 'shield', shieldduration)
                            specialtext = str("AND allows " + target + " to take no damage for the next " + str(shieldduration) + " duels.")
                        if magicusage == 'health' or magicusage == 'shield':
                            damageorhealth = "healing"
                            damageorhealthb = 'health'
                    if instigator == target:
                        displaymsg = str(instigator + " uses magic " + magicusage + " " + damageorhealth + " " + str(abs(damagedealt)) + " " + damageorhealthb + " " + specialtext + " " + magickilled)
                    else:
                        displaymsg = str(instigator + " uses magic " + magicusage + " on " + target + " " + damageorhealth + " " + str(abs(damagedealt)) + " " + damageorhealthb + " " + specialtext + " " + magickilled)
                    bot.say(str(displaymsg))
                    if not inchannel.startswith("#") and target != instigator:
                        bot.notice(str(displaymsg), target)
            mana = get_database_value(bot, instigator, 'mana')
            if mana <= 0:
                set_database_value(bot, instigator, 'mana', None)
            
        ## If not a command above, invalid
        else:
            bot.notice(instigator + ", It looks like " + str(commandortarget) + " is either not here, or not a valid person.", instigator)
    
    ## warning if user doesn't have duels enabled
    elif commandortarget.lower() not in dueloptedinarray:
        bot.notice(instigator + ", It looks like " + commandortarget + " has duels off.", instigator)
      
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
    
    ## Current Streaks
    winner_loss_streak, loser_win_streak = get_current_streaks(bot, winner, loser)
    
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
        XPearnedwinner = XPearnedwinnerranger
    else:
        XPearnedwinner = XPearnedwinnerstock
    yourclassloser = get_database_value(bot, loser, 'class') or 'notclassy'
    if yourclassloser == 'ranger':
        XPearnedloser = XPearnedloserranger
    else:
        XPearnedloser = XPearnedloserstock
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
    loserclass = get_database_value(bot, loser, 'class') or 'notclassy'
    # rogues don't take damage from the bot or themselves
    if loserclass == 'rogue':
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
        loserclass = get_database_value(bot, loser, 'class') or 'notclassy'
        ## Barbarians get a 50/50 chance of getting loot even if they lose
        barbarianstealroll = randint(0, 100)
        if loserclass == 'barbarian' and barbarianstealroll >= 50:
            lootwinnermsgb = str(loser + " steals the " + str(loot))
            adjust_database_value(bot, loser, loot, defaultadjust)
        elif winner == target:
            lootwinnermsgb = str(winner + " gains the " + str(loot))
            adjust_database_value(bot, winner, loot, defaultadjust)
        else:
            adjust_database_value(bot, winner, loot, defaultadjust)
    
    # Streaks Text
    streaktext = ''
    if instigator != target:
        streaktext = get_streaktext(bot, winner, loser, winner_loss_streak, loser_win_streak) or ''
        if streaktext != '':
            streaktext = str(str(streaktext) + "       ")

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
        
        
## 30 minute automation
@sopel.module.interval(1800)
def halfhourtimer(bot):
    
    ## bot does not need stats or backpack items
    refreshbot(bot)
    
    ## Clear Last Instigator
    set_database_value(bot, channel, 'lastinstigator', None)
    
    ## Who gets to win a mysterypotion?
    randomtargetarray = []
    lasttimedlootwinner = get_database_value(bot, channel, 'lasttimedlootwinner') or bot.nick
    for channel in bot.channels:
        for u in bot.privileges[channel.lower()]:
            targetdisenable = get_database_value(bot, u, 'disenable')
            if targetdisenable and target != lasttimedlootwinner and u != bot.nick:
                
                ## award coins to everyone
                adjust_database_value(bot, u, 'coins', halfhourcoinaward)
                
                ## mages regen mana
                yourclass = get_database_value(bot, u, 'class') or 'notclassy'
                if yourclass == 'mage':
                    mana = get_database_value(bot, u, 'mana')
                    if int(mana) < magemanaregenmax:
                        adjust_database_value(bot, u, 'mana', magemanaregen)
                        mana = get_database_value(bot, u, 'mana')
                        if int(mana) > magemanaregenmax:
                            set_database_value(bot, u, 'mana', magemanaregenmax)
                
                ## health regenerates for all
                health = get_database_value(bot, u, 'health')
                if int(health) < healthregenmax:
                    adjust_database_value(bot, u, 'health', healthregen)
                    health = get_database_value(bot, u, 'health')
                    if int(health) > healthregenmax:
                        set_database_value(bot, u, 'health', healthregenmax)
                        
        ########## select a winner
                randomtargetarray.append(u)
        if randomtargetarray == []:
            dummyvar = 1
        else:
            target = get_trigger_arg(randomtargetarray, 'random')
            loot = 'mysterypotion'
            loot_text = get_lootitem_text(bot, target, loot)
            adjust_database_value(bot, target, loot, defaultadjust)
            lootwinnermsg = str(target + ' is awarded a ' + str(loot) + ' ' + str(loot_text))
            bot.notice(lootwinnermsg, target)
            set_database_value(bot, channel, 'lasttimedlootwinner', target)
            
        
## Functions ######################################################################################################################

######################
## Criteria to duel ##
######################

def mustpassthesetoduel(bot, trigger, instigator, target, inchannel, channel, dowedisplay):
    displaymsg = ''
    executedueling = 0
    instigatorlastfought = get_database_value(bot, instigator, 'lastfought') or ''
    instigatordisenable = get_database_value(bot, instigator, 'disenable') or ''
    targetdisenable = get_database_value(bot, target, 'disenable') or ''
    instigatortime = get_timesince_duels(bot, instigator, 'timeout') or ''
    targettime = get_timesince_duels(bot, target, 'timeout') or ''
    channeltime = get_timesince_duels(bot, channel, 'timeout') or ''
    channellastinstigator = get_database_value(bot, channel, 'lastinstigator') or bot.nick
    
    if not inchannel.startswith("#"):
        displaymsg = str(instigator + " Duels must be in channel.")
    elif instigator == channellastinstigator and not bot.nick.endswith(devbot):
        displaymsg = str(instigator + ', You may not instigate fights twice in a row within a half hour.')
    elif target == instigatorlastfought and not bot.nick.endswith(devbot):
        displaymsg = str(instigator + ', You may not fight the same person twice in a row.')
    elif not instigatordisenable:
        displaymsg = str(instigator + ", It looks like you have disabled Challenges. Run .challenge on to re-enable.")
    elif not targetdisenable:
        displaymsg = str(instigator + ', It looks like ' + target + ' has disabled Challenges.')
    elif instigatortime <= USERTIMEOUT and not bot.nick.endswith(devbot):
        displaymsg = str("You can't challenge for %d seconds." % (USERTIMEOUT - instigatortime))
    elif targettime <= USERTIMEOUT and not bot.nick.endswith(devbot):
        displaymsg = str(target + " can't challenge for %d seconds." % (USERTIMEOUT - targettime))
    elif channeltime <= CHANTIMEOUT and not bot.nick.endswith(devbot):
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
    oldvalue = get_database_value(bot, nick, databasekey) or 0
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
    set_database_value(bot, nick, databasekey, None)
    adjustarray = []
    if adjustmentdirection == 'add':
        adjustarraynew.append(entry)
    elif adjustmentdirection == 'del':
        adjustarraynew.remove(entry)
    for x in adjustarraynew:
        if x not in adjustarray:
            adjustarray.append(x)
    if adjustarray == []:
        set_database_value(bot, nick, databasekey, None)
    else:
        set_database_value(bot, nick, databasekey, adjustarray)
    
###################
## Living Status ##
###################

def whokilledwhom(bot, winner, loser):
    ## Reset mana and health
    set_database_value(bot, loser, 'mana', None)
    set_database_value(bot, loser, 'health', stockhealth)
    ## update kills/deaths
    adjust_database_value(bot, winner, 'kills', defaultadjust)
    adjust_database_value(bot, loser, 'respawns', defaultadjust)
    ## Loot Corpse
    loserclass = get_database_value(bot, loser, 'class') or 'notclassy'
    ## rangers don't lose their stuff
    if loserclass != 'ranger':
        for x in lootitemsarray:
            gethowmany = get_database_value(bot, loser, x)
            adjust_database_value(bot, winner, x, gethowmany)
            set_database_value(bot, loser, x, None)

def healthcheck(bot, nick):
    health = get_database_value(bot, nick, 'health')
    if not health and nick != bot.nick:
        set_database_value(bot, nick, 'health', stockhealth)
    mana = get_database_value(bot, nick, 'mana')
    if int(mana) <= 0:
        set_database_value(bot, nick, 'mana', None)

def refreshbot(bot):
    set_database_value(bot, bot.nick, 'disenable', botonoffstatus)
    for x in challengestatsadminarray:
        statset = x
        if statset != 'disenable':
            set_database_value(bot, bot.nick, x, None)
            
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
    set_database_value(bot, nick, oppositestreaktype, None)
    
def get_current_streaks(bot, winner, loser):
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

def randominventory(bot, instigator):
    yourclass = get_database_value(bot, instigator, 'class') or 'notclassy'
    if yourclass == 'scavenger':
        randomfindchance = randint(scavegerfindpercent, 100)
    else:
        randomfindchance = randint(0, 120)
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
        loot_text = str(": worth " + str(healthpotionworth) + " health.")
    elif loottype == 'poisonpotion':
        loot_text = str(": worth " + str(poisonpotionworth) + " health.")
    elif loottype == 'manapotion':
        loot_text = str(": worth " + str(manapotionworth) + " health.")
    elif loottype == 'timepotion':
        loot_text = ': worth up to ' + str(USERTIMEOUT) + ' seconds of timeout.'
    elif loottype == 'mysterypotion':
        loot_text = ': The label fell off. Use at your own risk!'
    else:
        loot_text = ''
    if loot_text != '':
        loot_text = str(loot_text + " Use .challenge loot use " + str(loottype) + " to consume.")
    return loot_text
  
######################
## Weapon Selection ##
######################

## allchan weapons
def getallchanweaponsrandom(bot, channel):
    allchanweaponsarray = []
    for u in bot.channels[channel].users:
        weaponslist = get_database_value(bot, u, 'weaponslocker') or ['fist']
        for x in weaponslist:
            allchanweaponsarray.append(x)
    weapon = get_trigger_arg(allchanweaponsarray, 'random')
    return weapon

def weaponofchoice(bot, nick):
    weaponslistselect = []
    weaponslist = get_database_value(bot, nick, 'weaponslocker') or []
    lastusedweaponarry = get_database_value(bot, nick, 'lastweaponusedarray') or []
    lastusedweapon = get_database_value(bot, nick, 'lastweaponused') or 'fist'
    for x in weaponslist:
        if x not in lastusedweaponarry and x != lastusedweapon:
            weaponslistselect.append(x)
    if weaponslistselect == [] and weaponslist != []:
        set_database_value(bot, nick, 'lastweaponusedarray', None)
        return weaponofchoice(bot, nick)
    weapon = get_trigger_arg(weaponslistselect, 'random') or 'fist'
    adjust_database_array(bot, nick, weapon, 'lastweaponusedarray', 'add')
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
    winnerclass = get_database_value(bot, winner, 'class') or 'notclassy'
    ## Bot deals a set amount
    if winner == bot.nick:
        rando = botdamage
    ## Barbarians get extra damage
    elif winnerclass == 'barbarian':
        rando = randint(barbarianminimumdamge, 120)
    else:
        rando = randint(0, 120)
    # magic shield
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
    nickshield = get_database_value(bot, nick, 'shield')
    if nick == bot.nick:
        pepper = 'Dragon Breath Chilli'
    elif nickcurse or nickshield:
        peppercurse = ''
        peppershield = ''
        if nickcurse:
            peppercurse = 'Cursed '
        if nickshield:
            peppershield = 'Shield'
        pepper = str(peppercurse + peppershield)
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
            instigatorfightroll = randint(0, 20)
        instigatorfightarray.append(instigatorfightroll)
        instigatorfight = int(instigatorfight) - 1
    instigatorfight = max(instigatorfightarray)
    while int(targetfight) > 0:
        if targetyourclass == 'rogue':
            targetfightroll = randint(10, 22)
        else:
            targetfightroll = randint(0, 19)
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
        if totalarray > 1:
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
    elif number == 'random':
        if totalarray > 1:
            randomselected = random.randint(0,len(triggerargsarray) - 1)
            triggerarg = str(triggerargsarray [randomselected])
    elif number == 'list':
        for x in triggerargsarray:
            if triggerarg != '':
                triggerarg  = str(triggerarg  + ", " + x)
            else:
                triggerarg  = str(x)
    else:
        number = int(number) - 1
        try:
            triggerarg = triggerargsarray[number]
        except IndexError:
            triggerarg = ''
    return triggerarg
