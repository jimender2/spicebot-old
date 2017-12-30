#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
from sopel.module import OP
from sopel.module import ADMIN
from sopel.module import VOICE
import sopel
from sopel import module, tools
import random
from random import randint
import time
import datetime
import re
import sys
import os
from os.path import exists

## not needed if using without spicebot
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

###################
## Configurables ##
###################

## Timeouts
USERTIMEOUT = 180 ## Time between a users ability to duel - 3 minutes
CHANTIMEOUT = 40 ## Time between duels in a channel - 40 seconds
OPTTIMEOUT = 1800 ## Time between opting in and out of the game - Half hour
ASSAULTTIMEOUT = 1800 ## Time Between Full Channel Assaults
COLOSSEUMTIMEOUT = 1800 ## Time Between colosseum events
CLASSTIMEOUT = 86400 ## Time between changing class - One Day

## Half hour timer
halfhourcoinaward = 10 ## coin gain per half hour
magemanaregen = 50 ## mages regenerate mana: rate
magemanaregenmax = 500 ## mages regenerate mana: limit
healthregen = 50 ## health regen rate
healthregenmax = 500 ## health regen limit

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
lootsellrewardscavenger = 30 ## coin rewarded in selling loot for scavengers
lootsellreward = 25 ## normal coin rewarded in selling loot
changeclasscost = 100 ## ## how many coin to change class

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
XPearnedwinnerranger = 7 ## xp earned as a winner and ranger
XPearnedloserranger = 5 ## xp earned as a loser and ranger
XPearnedwinnerstock = 5 ## default xp earned as a winner
XPearnedloserstock = 3 ## default xp earned as a loser

## Class advantages
scavegerfindpercent = 40 ## scavengers have a higher percent chance of finding loot
barbarianminimumdamge = 40 ## Barbarians always strike a set value or above

## Bot
botdamage = 150 ## The bot deals a set damage
duelrecorduser = 'duelrecorduser' ## just a database column to store values in
devbot = 'dev' ## If using a development bot and want to bypass commands, this is what the bots name ends in

## other
bugbountycoinaward = 100 ## users that find a bug in the code, get a reward
defaultadjust = 1 ## The default number to increase a stat
GITWIKIURL = "https://github.com/deathbybandaid/sopel-modules/wiki/Duels" ## Wiki URL
stockhealth = 1000 ## default health for new players and respawns

############
## Arrays ##
############

botdevteam = ['deathbybandaid','DoubleD','Mace_Whatdo','dysonparkes','PM','under_score'] ## people to recognize
lootitemsarray = ['healthpotion','manapotion','poisonpotion','timepotion','mysterypotion'] ## types of potions
backpackarray = ['coin','healthpotion','manapotion','poisonpotion','timepotion','mysterypotion'] ## how to organize backpack
duelstatsarray = ['class','health','curse','shield','mana','xp','wins','losses','winlossratio','respawns','kills','lastfought','timeout']
statsbypassarray = ['winlossratio','timeout'] ## stats that use their own functions to get a value
transactiontypesarray = ['buy','sell','trade','use','inv'] ## valid commands for loot
classarray = ['barbarian','mage','scavenger','rogue','ranger'] ## Valid Classes
duelstatsadminarray = ['shield','classtimeout','class','curse','bestwinstreak','worstlosestreak','opttime','coin','wins','losses','health','mana','healthpotion','mysterypotion','timepotion','respawns','xp','kills','timeout','poisonpotion','manapotion','lastfought','konami'] ## admin settings
statsadminchangearray = ['set','reset'] ## valid admin subcommands


################################################################################
## Main Operation #### Main Operation #### Main Operation #### Main Operation ##
################################################################################

## work with /me ACTION (does not work with manual weapon)
@module.rule('^(?:challenges|(?:fi(?:ght|te)|duel)s(?:\s+with)?)\s+([a-zA-Z0-9\[\]\\`_\^\{\|\}-]{1,32}).*')
@module.intent('ACTION')
@module.require_chanmsg
def duel_action(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'duel')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)

## Base command
@sopel.module.commands('duel','challenge')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'duel')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)

## The Command Process
def execute_main(bot, trigger, triggerargsarray):

    ## Initial ARGS of importance
    fullcommandused = get_trigger_arg(triggerargsarray, 0)
    commandortarget = get_trigger_arg(triggerargsarray, 1)
    dowedisplay = 0
    displaymessage = ''
    typeofduel = 'target'
    
    ## Build User/channel Arrays
    botownerarray, operatorarray, voicearray, adminsarray, allusersinroomarray = special_users(bot)
    dueloptedinarray = get_database_value(bot, bot.nick, 'duelusers') or []
    allusersinroomarray, classcantchangearray, canduelarray, targetarray, targetcantoptarray = [], [], [], [], []
    for u in bot.users:
        allusersinroomarray.append(u)
    for u in allusersinroomarray:
        inchannel = "#bypass"
        canduel = mustpassthesetoduel(bot, trigger, u, u, inchannel, dowedisplay)
        if canduel and u != bot.nick:
            canduelarray.append(u)
        opttime = get_timesince_duels(bot, u, 'optime')
        if opttime < OPTTIMEOUT and not bot.nick.endswith(devbot):
            targetcantoptarray.append(u)
        classtime = get_timesince_duels(bot, u, 'classtimeout')
        if classtime < CLASSTIMEOUT and not bot.nick.endswith(devbot):
            classcantchangearray.append(u)
            
    ###### Channel
    inchannel = trigger.sender

    ## Array Totals
    canduelarraytotal = len(canduelarray)
    dueloptedinarraytotal = len(dueloptedinarray)
    allusersinroomarraytotal = len(allusersinroomarray)

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
    instigatorclass = get_database_value(bot, instigator, 'class')
    instigatorclasstime = get_timesince_duels(bot, instigator, 'classtimeout')
    ##tempfix
    instigatorcoins = get_database_value(bot, instigator, 'coins') or 0
    if instigatorcoins:
        adjust_database_value(bot, instigator, 'coin', instigatorcoins)
        set_database_value(bot, instigator, 'coins', None)
    instigatorcoin = get_database_value(bot, instigator, 'coin') or 0
        

    ## Information
    adjust_database_value(bot, duelrecorduser, 'usage', 1)
    duelrecordusertime = get_timesince_duels(bot, duelrecorduser, 'timeout') or CHANTIMEOUT
    duelrecorduserlastinstigator = get_database_value(bot, duelrecorduser, 'lastinstigator') or bot.nick
    lastfullroomassult = get_timesince_duels(bot, duelrecorduser, 'lastfullroomassult') or ASSAULTTIMEOUT
    lastfullroomassultinstigator = get_database_value(bot, duelrecorduser, 'lastfullroomassultinstigator') or bot.nick
    lastfullroomcolosseum = get_timesince_duels(bot, duelrecorduser, 'lastfullroomcolosseum') or ASSAULTTIMEOUT
    lastfullroomcolosseuminstigator = get_database_value(bot, duelrecorduser, 'lastfullroomcolosseuminstigator') or bot.nick

    ## The only commands that should get through if instigator doesn't have duels enabled
    commandbypassarray = ['on','off']

    ## If Not a target or a command used
    if not fullcommandused:
        bot.notice(instigator + ", Who did you want to duel? Online Docs: " + GITWIKIURL, instigator)

    ## commands cannot be run if opted out
    elif instigator not in dueloptedinarray and commandortarget not in commandbypassarray:
        bot.notice(instigator + ", It looks like you have duels off.", instigator)

    ## Bot
    elif commandortarget == bot.nick:
        bot.say("I refuse to fight a biological entity!")

    ## yourself
    elif commandortarget == instigator:
        bot.say("If you are feeling self-destructive, there are places you can call.")

    ## Determine if the arg after .duel is a target or a command
    elif commandortarget.lower() not in [x.lower() for x in allusersinroomarray]:
        commandortarget = commandortarget.lower()

        ## Docs
        if commandortarget == 'docs' or commandortarget == 'help' or commandortarget == 'help':
            target = get_trigger_arg(triggerargsarray, 2)
            if not target:
                bot.say("Online Docs: " + GITWIKIURL)
            elif target.lower() not in [x.lower() for x in allusersinroomarray]:
                bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
            else:
                bot.notice("Online Docs: " + GITWIKIURL, target)

        ## On/off
        elif commandortarget == 'on' or commandortarget == 'off':
            target = get_trigger_arg(triggerargsarray, 2) or instigator
            targetopttime = get_timesince_duels(bot, target, 'opttime')
            if target.lower() not in [x.lower() for x in allusersinroomarray] and target != 'everyone':
                bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
            elif target != instigator and instigator not in adminsarray:
                bot.notice(instigator + "This is an admin only function.", instigator)
            elif target == 'everyone':
                for u in allusersinroomarray:
                    if commandortarget == 'on':
                        adjust_database_array(bot, bot.nick, target, 'duelusers', 'add')
                    else:
                        adjust_database_array(bot, bot.nick, target, 'duelusers', 'del')
                bot.notice(instigator + ", duels should now be " +  commandortarget + ' for ' + target + '.', instigator)
            elif target in targetcantoptarray:
                bot.notice(instigator + " It looks like " + target + " can't enable/disable duels for %d seconds." % (OPTTIMEOUT - targetopttime), instigator)
            elif commandortarget == 'on' and target.lower() in [x.lower() for x in dueloptedinarray]:
                bot.notice(instigator + ", It looks like " + target + " already has duels on.", instigator)
            elif commandortarget == 'off' and target.lower() not in [x.lower() for x in dueloptedinarray]:
                bot.notice(instigator + ", It looks like " + target + " already has duels off.", instigator)
            else:
                if commandortarget == 'on':
                    adjust_database_array(bot, bot.nick, target, 'duelusers', 'add')
                else:
                    adjust_database_array(bot, bot.nick, target, 'duelusers', 'del')
                set_database_value(bot, target, 'opttime', now)
                bot.notice(instigator + ", duels should now be " +  commandortarget + ' for ' + target + '.', instigator)

        ## Usage
        elif commandortarget == 'usage':
            target = get_trigger_arg(triggerargsarray, 2) or instigator
            targetname = target
            if target == 'channel':
                target = duelrecorduser
            totaluses = get_database_value(bot, target, 'usage')
            bot.say(targetname + " has used duels " + str(totaluses) + " times.")

        ## Random Dueling
        elif commandortarget == 'random':
            if canduelarray == []:
                bot.notice(instigator + ", It looks like the random target finder has failed.", instigator)
            elif not inchannel.startswith("#"):
                bot.notice(instigator + " Duels must be in a channel.", instigator)
            else:
                target = get_trigger_arg(canduelarray, 'random')
                OSDTYPE = 'say'
                return getreadytorumble(bot, trigger, instigator, target, OSDTYPE, fullcommandused, now, triggerargsarray, typeofduel, botownerarray, operatorarray, voicearray, adminsarray)

        ## Colosseum
        elif commandortarget == 'colosseum':
            nickarray = []
            for x in canduelarray:
                if x != bot.nick:
                    nickarray.append(x)
            nickarraytotal = len(nickarray)
            if lastfullroomcolosseum < COLOSSEUMTIMEOUT and not bot.nick.endswith(devbot):
                bot.notice(instigator + ", colosseum can't be used for %d seconds." % (COLOSSEUMTIMEOUT - lastfullroomcolosseum), instigator)
            elif lastfullroomcolosseuminstigator == instigator and not bot.nick.endswith(devbot):
                bot.notice(instigator + ", You may not instigate a colosseum event twice in a row.", instigator)
            elif not inchannel.startswith("#"):
                bot.notice(instigator + " Duels must be in channel.", instigator)
            elif instigator not in canduelarray:
                bot.notice(instigator + ", It looks like you can't duel right now.", instigator)
            elif nickarray == []:
                bot.notice(instigator + ", It looks like the colosseum target finder has failed.", instigator)
            else:
                displaymessage = get_trigger_arg(nickarray, "list")
                bot.say(instigator + " Initiated a colosseum event. Good luck to " + displaymessage)
                duelrecorduserpot = 100
                winner = selectwinner(bot, nickarray)
                bot.say("The Winner is: " + winner + "! Total winnings: " + str(duelrecorduserpot) + " coin! Losers took " + str(duelrecorduserpot) + " damage")
                diedinbattle = []
                for x in nickarray:
                    if x != winner:
                        adjust_database_value(bot, x, 'health', -abs(duelrecorduserpot))
                        currenthealth = get_database_value(bot, x, 'health')
                        if currenthealth <= 0:
                            whokilledwhom(bot, winner, x)
                            diedinbattle.append(x)
                displaymessage = get_trigger_arg(diedinbattle, "list")
                if displaymessage:
                    bot.say(displaymessage + " died in this event.")
                adjust_database_value(bot, winner, 'colosseum_pot', duelrecorduserpot)
                set_database_value(bot, duelrecorduser, 'lastfullroomcolosseum', now)
                set_database_value(bot, duelrecorduser, 'lastfullroomcolosseuminstigator', instigator)

        ## Duel Everyone
        elif commandortarget == 'assault' or commandortarget == 'everyone':
            fullchanassaultarray = []
            for x in canduelarray:
                if x != instigator and x != bot.nick:
                    fullchanassaultarray.append(x)
            fullchanassaultarraytotal = len(fullchanassaultarray)
            if lastfullroomassult < ASSAULTTIMEOUT and not bot.nick.endswith(devbot):
                bot.notice(instigator + ", Full Channel Assault can't be used for %d seconds." % (ASSAULTTIMEOUT - lastfullroomassult), instigator)
            elif lastfullroomassultinstigator == instigator and not bot.nick.endswith(devbot):
                bot.notice(instigator + ", You may not instigate a Full Channel Assault twice in a row.", instigator)
            elif not inchannel.startswith("#"):
                bot.notice(instigator + " Duels must be in a channel.", instigator)
            elif instigator not in canduelarray:
                bot.notice(instigator + ", It looks like you can't duel right now.", instigator)
            elif fullchanassaultarray == []:
                bot.notice(instigator + ", It looks like the Full Channel Assault target finder has failed.", instigator)
            else:
                OSDTYPE = 'notice'
                displaymessage = get_trigger_arg(fullchanassaultarray, "list")
                bot.say(instigator + " Initiated a Full Channel Assault. Good luck to " + displaymessage)
                set_database_value(bot, duelrecorduser, 'lastfullroomassult', now)
                set_database_value(bot, duelrecorduser, 'lastfullroomassultinstigator', instigator)
                lastfoughtstart = get_database_value(bot, instigator, 'lastfought')
                typeofduel = 'assault'
                return getreadytorumble(bot, trigger, instigator, fullchanassaultarray, OSDTYPE, fullcommandused, now, triggerargsarray, typeofduel, botownerarray, operatorarray, voicearray, adminsarray)
                set_database_value(bot, instigator, 'lastfought', lastfoughtstart)

        ## War Room
        elif commandortarget == 'warroom':
            inchannel = "#bypass"
            dowedisplay = 1
            subcommand = get_trigger_arg(triggerargsarray, 2)
            if not subcommand:
                if instigator in canduelarray:
                    bot.notice(instigator + ", It looks like you can duel.", instigator)
                else:
                    mustpassthesetoduel(bot, trigger, instigator, instigator, inchannel, dowedisplay)
            elif subcommand == 'colosseum':
                if lastfullroomcolosseuminstigator == instigator and not bot.nick.endswith(devbot):
                    bot.notice(instigator + ", You may not instigate a colosseum event twice in a row.", instigator)
                elif lastfullroomcolosseum < COLOSSEUMTIMEOUT and not bot.nick.endswith(devbot):
                    bot.notice(instigator + ", colosseum event can't be used for %d seconds." % (ASSAULTTIMEOUT - lastfullroomassult), instigator)
                else:
                    bot.notice(instigator + ", colosseum event can be used.", instigator)
            elif subcommand == 'assault' or subcommand == 'everyone':
                if lastfullroomassultinstigator == instigator and not bot.nick.endswith(devbot):
                    bot.notice(instigator + ", You may not instigate a Full Channel Assault twice in a row.", instigator)
                elif lastfullroomassult < ASSAULTTIMEOUT and not bot.nick.endswith(devbot):
                    bot.notice(instigator + ", Full Channel Assault can't be used for %d seconds." % (ASSAULTTIMEOUT - lastfullroomassult), instigator)
                else:
                    bot.notice(instigator + ", Full Channel Assault can be used.", instigator)
            elif subcommand == 'list':
                displaymessage = get_trigger_arg(canduelarray, "list")
                bot.say(instigator + ", you may duel the following users: "+ str(displaymessage ))
            elif subcommand.lower() not in allusersinroomarray:
                bot.notice(instigator + ", It looks like " + str(subcommand) + " is either not here, or not a valid person.", instigator)
            else:
                if subcommand in canduelarray:
                    bot.notice(instigator + ", It looks like you can duel " + subcommand + ".", instigator)
                else:
                    mustpassthesetoduel(bot, trigger, instigator, subcommand, inchannel, dowedisplay)

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
                bot.say("You may not change your class more than once per 24 hours. Please wait %d seconds to change." % (CLASSTIMEOUT - instigatorclasstime))
            elif subcommand not in subcommandarray:
                bot.say("Invalid command. Options are set or change.")
            elif not setclass:
                bot.say("Which class would you like to use? Options are: " + classes +".")
            elif subcommand == 'set' and instigatorclass:
                bot.say("Your class is currently set to " + str(instigatorclass) + ". Use .duel class change    to change class. Options are : " + classes + ".")
            elif subcommand == 'change' and instigatorcoin < changeclasscost:
                bot.say("Changing class costs " + str(changeclasscost) + " coin.")
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
                        adjust_database_value(bot, instigator, 'coin', -abs(changeclasscost))

        ## Streaks
        elif commandortarget == 'streaks':
            target = get_trigger_arg(triggerargsarray, 2) or instigator
            if target.lower() not in [x.lower() for x in allusersinroomarray]:
                bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
            elif target.lower() not in [x.lower() for x in dueloptedinarray]:
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
            if target.lower() not in [x.lower() for x in allusersinroomarray]:
                bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
            elif target.lower() not in [x.lower() for x in dueloptedinarray]:
                bot.notice(instigator + ", It looks like " + target + " has duels off.", instigator)
            else:
                for x in backpackarray:
                    gethowmany = get_database_value(bot, target, x)
                    if gethowmany:
                        if gethowmany == 1:
                            loottype = str(x)
                        else:
                            loottype = str(str(x)+"s")
                        addstat = str(' ' + str(loottype) + "=" + str(gethowmany))
                        displaymessage = str(displaymessage + addstat)
                if displaymessage != '':
                    displaymessage = str(target + "'s " + commandortarget + ":" + displaymessage)
                    bot.say(displaymessage)
                else:
                    bot.say(instigator + ", It looks like " + target + " has no " +  commandortarget + ".", instigator)

        ## Stats
        elif commandortarget == 'stats':
            target = get_trigger_arg(triggerargsarray, 2) or instigator
            if target.lower() not in [x.lower() for x in allusersinroomarray]:
                bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
            elif target.lower() not in [x.lower() for x in dueloptedinarray]:
                bot.notice(instigator + ", It looks like " + target + " has duels off.", instigator)
            else:
                for x in duelstatsarray:
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
                if u.lower() in [x.lower() for x in allusersinroomarray]:
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
                bot.notice(instigator + ", Do you want to buy, sell, trade, inv, or use?", instigator)
            elif lootcommand not in transactiontypesarray:
                bot.notice(instigator + ", Do you want to buy, sell, trade, inv, or use?", instigator)
            elif lootcommand == 'inv':
                target = get_trigger_arg(triggerargsarray, 3) or instigator
                if target.lower() not in [x.lower() for x in allusersinroomarray]:
                    bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
                elif target.lower() not in [x.lower() for x in dueloptedinarray]:
                    bot.notice(instigator + ", It looks like " + target + " has duels off.", instigator)
                else:
                    for x in backpackarray:
                        gethowmany = get_database_value(bot, target, x)
                        if gethowmany:
                            if gethowmany == 1:
                                loottype = str(x)
                            else:
                                loottype = str(str(x)+"s")
                            addstat = str(' ' + str(loottype) + "=" + str(gethowmany))
                            displaymessage = str(displaymessage + addstat)
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
                elif target.lower() not in [x.lower() for x in allusersinroomarray]:
                    bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
                elif target == bot.nick:
                  bot.notice(instigator + ", I am immune to " + lootitem, instigator)
                elif target.lower() not in [x.lower() for x in dueloptedinarray]:
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
                            duelrecorduserlastinstigator = get_database_value(bot, duelrecorduser, 'lastinstigator') or bot.nick
                            if duelrecorduserlastinstigator == target:
                                set_database_value(bot, duelrecorduser, 'lastinstigator', None)
                            set_database_value(bot, target, 'timeout', None)
                            set_database_value(bot, duelrecorduser, 'timeout', None)
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
                    while int(quantity) > 0:
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
                    coinrequired = lootbuycostscavenger * int(quantity)
                else:
                    coinrequired = lootbuycost * int(quantity)
                if instigatorcoin < coinrequired:
                    bot.notice(instigator + ", You do not have enough coin for this action.", instigator)
                else:
                    while int(quantity) > 0:
                        quantity = int(quantity) - 1
                        if instigatorclass == 'scavenger':
                            cost = lootbuycostscavenger
                        else:
                            cost = lootbuycost
                        reward = 1
                        itemtoexchange = 'coin'
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
                        itemexchanged = 'coin'
                        adjust_database_value(bot, instigator, itemtoexchange, cost)
                        adjust_database_value(bot, instigator, itemexchanged, reward)
                    bot.notice(instigator + ", " + str(lootcommand) + " Completed.", instigator)

        ## Konami
        elif commandortarget == 'upupdowndownleftrightleftrightba':
            konami = get_database_value(bot, instigator, 'konami')
            if not konami:
                set_database_value(bot, instigator, 'konami', 1)
                bot.notice(instigator + " you have found the cheatcode easter egg!!!", instigator)
                konamiset = 600
                adjust_database_value(bot, instigator, 'health', konamiset)
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
            elif adjustmentdirection == 'inv' and inchannel.startswith("#"):
                gethowmany = get_database_array_total(bot, target, 'weaponslocker')
                bot.say(instigator + ' has ' + str(gethowmany) + "weapons in their locker. They Can be viewed in privmsg by running .duel weaponslocker inv view")
            elif adjustmentdirection == 'inv' and not inchannel.startswith("#"):
                if not weaponchange:
                    gethowmany = get_database_array_total(bot, target, 'weaponslocker')
                    bot.say(instigator + ' has ' + str(gethowmany) + "weapons in their locker. They Can be viewed in privmsg by running .duel weaponslocker inv view")
                elif weaponchange == 'view':
                    weapons = get_trigger_arg(weaponslist, 'list')
                chunks = weapons.split()
                per_line = 20
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
            targetcurse = get_database_value(bot, target, 'curse') or 0
            targetshield = get_database_value(bot, target, 'shield') or 0
            if not magicusage:
                bot.say('Magic uses include: attack, instakill, health, curse, shield')
            elif magicusage not in magicoptions:
                bot.say('Magic uses include: attack, instakill, health, curse, shield')
            elif target.lower() not in [x.lower() for x in allusersinroomarray]:
                bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
            elif target == bot.nick:
                bot.notice(instigator + ", I am immune to magic " + magicusage, instigator)
            elif target.lower() not in [x.lower() for x in dueloptedinarray]:
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

        ## Admin Commands
        elif commandortarget == 'admin' and instigator not in adminsarray:
            bot.notice(instigator + ", This is an admin only functionality.", instigator)
        elif commandortarget == 'admin':
            subcommand = get_trigger_arg(triggerargsarray, 2)
            settingchange = get_trigger_arg(triggerargsarray, 3)
            if not subcommand:
                bot.notice(instigator + ", What Admin change do you want to make?", instigator)
            elif subcommand == 'channel':
                if not settingchange:
                    bot.notice(instigator + ", What channel setting do you want to change?", instigator)
                elif settingchange == 'lastassault':
                    set_database_value(bot, duelrecorduser, 'lastfullroomassultinstigator', None)
                    bot.notice("Last Assault Instigator removed.", instigator)
                    set_database_value(bot, duelrecorduser, 'lastfullroomassult', None)
                elif settingchange == 'lastroman':
                    set_database_value(bot, duelrecorduser, 'lastfullroomcolosseuminstigator', None)
                    bot.notice("Last Colosseum Instigator removed.", instigator)
                    set_database_value(bot, duelrecorduser, 'lastfullroomcolosseum', None)
                elif settingchange == 'lastinstigator':
                    set_database_value(bot, duelrecorduser, 'lastinstigator', None)
                    bot.notice("Last Fought Instigator removed.", instigator)
                elif settingchange == 'halfhoursim':
                    bot.notice("Simulating the half hour automated events.", instigator)
                    halfhourtimer(bot)
                else:
                    bot.notice("Must be an invalid command.", instigator)
            elif subcommand == 'stats':
                incorrectdisplay = "A correct command use is .duel admin stats target set/reset stat"
                target = get_trigger_arg(triggerargsarray, 3)
                subcommand = get_trigger_arg(triggerargsarray, 4)
                statset = get_trigger_arg(triggerargsarray, 5)
                newvalue = get_trigger_arg(triggerargsarray, 6) or None
                if not target:
                    bot.notice(instigator + ", Target Missing. " + incorrectdisplay, instigator)
                elif target.lower() not in [x.lower() for x in allusersinroomarray] and target != 'everyone':
                    bot.notice(instigator + ", It looks like " + str(target) + " is either not here, or not a valid person.", instigator)
                elif not subcommand:
                    bot.notice(instigator + ", Subcommand Missing. " + incorrectdisplay, instigator)
                elif subcommand not in statsadminchangearray:
                    bot.notice(instigator + ", Invalid subcommand. " + incorrectdisplay, instigator)
                elif not statset:
                    bot.notice(instigator + ", Stat Missing. " + incorrectdisplay, instigator)
                elif statset not in duelstatsadminarray and statset != 'all':
                    bot.notice(instigator + ", Invalid stat. " + incorrectdisplay, instigator)
                elif instigator not in adminsarray:
                    bot.notice(instigator + "This is an admin only function.", instigator)
                else:
                    if subcommand == 'reset':
                        newvalue = None
                    if subcommand == 'set' and newvalue == None:
                        bot.notice(instigator + ", When using set, you must specify a value. " + incorrectdisplay, instigator)
                    elif target == 'everyone':
                        for u in bot.users:
                            if statset == 'all':
                                for x in duelstatsadminarray:
                                    set_database_value(bot, u, x, newvalue)
                            else:
                                set_database_value(bot, u, statset, newvalue)
                        bot.notice(instigator + ", Possibly done Adjusting stat(s).", instigator)
                    else:
                        if statset == 'all':
                            for x in duelstatsadminarray:
                                set_database_value(bot, target, x, newvalue)
                        else:
                            set_database_value(bot, target, statset, newvalue)
                        bot.notice(instigator + ", Possibly done Adjusting stat(s).", instigator)
            elif subcommand == 'bugbounty':
                target = get_trigger_arg(triggerargsarray, 3)
                if not target:
                    bot.notice(instigator + ", Target Missing. ", instigator)
                elif target.lower() not in [x.lower() for x in allusersinroomarray]:
                    bot.notice(instigator + ", It looks like " + str(target) + " is either not here, or not a valid person.", instigator)
                elif instigator not in adminsarray:
                    bot.notice(instigator + "This is an admin only function.", instigator)
                else:
                    bot.say(target + ' is awarded ' + str(bugbountycoinaward) + " coin for finding a bug in duels.")
                    adjust_database_value(bot, target, 'coin', bugbountycoinaward)
            
                
        ## If not a command above, invalid
        else:
            bot.notice(instigator + ", It looks like " + str(commandortarget) + " is either not here, or not a valid person.", instigator)

    ## warning if user doesn't have duels enabled
    elif commandortarget.lower() not in [x.lower() for x in dueloptedinarray] and commandortarget != bot.nick:
        bot.notice(instigator + ", It looks like " + commandortarget + " has duels off.", instigator)

    else:
        OSDTYPE = 'say'
        target = get_trigger_arg(triggerargsarray, 1)
        dowedisplay = 1
        executedueling = mustpassthesetoduel(bot, trigger, instigator, target, inchannel, dowedisplay)
        if executedueling:
            return getreadytorumble(bot, trigger, instigator, target, OSDTYPE, fullcommandused, now, triggerargsarray, typeofduel, botownerarray, operatorarray, voicearray, adminsarray)

    ## bot does not need stats or backpack items
    refreshbot(bot)

def getreadytorumble(bot, trigger, instigator, targetarray, OSDTYPE, fullcommandused, now, triggerargsarray, typeofduel, botownerarray, operatorarray, voicearray, adminsarray):

    assaultstatsarray = ['wins','losses','potionswon','potionslost','kills','deaths','damagetaken','damagedealt','levelups','xp']
    ## clean empty stats
    assaultdisplay = ''
    assault_xp, assault_wins, assault_losses, assault_potionswon, assault_potionslost, assault_deaths, assault_kills, assault_damagetaken, assault_damagedealt, assault_levelups = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

    ## Target Array
    if not isinstance(targetarray, list):
        tempvar = targetarray
        targetarray = []
        targetarray.append(tempvar)
    targetarraytotal = len(targetarray)
    for target in targetarray:
        targetarraytotal = targetarraytotal - 1
        if typeofduel == 'assault':
            targetlastfoughtstart = get_database_value(bot, target, 'lastfought')

        ## Update Time Of Combat
        set_database_value(bot, instigator, 'timeout', now)
        set_database_value(bot, target, 'timeout', now)
        set_database_value(bot, duelrecorduser, 'timeout', now)

        ## Naming and Initial pepper level
        instigatorname, instigatorpepperstart = whatsyourname(bot, trigger, instigator, botownerarray, operatorarray, voicearray, adminsarray)
        if instigator == target:
            targetname = "themself"
            targetpepperstart = ''
        else:
            targetname, targetpepperstart = whatsyourname(bot, trigger, target, botownerarray, operatorarray, voicearray, adminsarray)

        ## Magic Attributes Start
        instigatorshieldstart, targetshieldstart, instigatorcursestart, targetcursestart = get_current_magic_attributes(bot, instigator, target)

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
                weapon = getallchanweaponsrandom(bot)
            elif weapon == 'target':
                weapon = weaponofchoice(bot, target)
                weapon = str(target + "'s " + weapon)

        ## Select Winner
        if target == bot.nick:
            winner = bot.nick
            loser = instigator
        else:
            nickarray = [instigator, target]
            winner = selectwinner(bot, nickarray)
            if winner == instigator:
                loser = target
            else:
                loser = instigator

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
        set_database_value(bot, duelrecorduser, 'lastinstigator', instigator)

        ## Update Health Of Loser, respawn, allow winner to loot
        adjust_database_value(bot, loser, 'health', damage)
        damage = abs(damage)
        currenthealth = get_database_value(bot, loser, 'health')
        if currenthealth <= 0:
            whokilledwhom(bot, winner, loser)
            if instigator == target:
                loser = targetname
            winnermsg = str(winner + ' killed ' + loser + weapon + ' forcing a respawn!!')
            if winner == instigator:
                assault_kills = assault_kills + 1
            else:
                assault_deaths = assault_deaths + 1
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
            assault_levelups = assault_levelups + 1
        if targetpeppernow != targetpepperstart and instigator != target:
            pepperstatuschangemsg = str(pepperstatuschangemsg + target + " graduates to " + targetpeppernow + "! ")

        ## Random Loot
        lootwinnermsg, lootwinnermsgb = '', ''
        randominventoryfind = randominventory(bot, instigator)
        if randominventoryfind == 'true' and target != bot.nick and instigator != target:
            loot = get_trigger_arg(lootitemsarray, 'random')
            loot_text = get_lootitem_text(bot, winner, loot)
            lootwinnermsg = str(instigator + ' found a ' + str(loot) + ' ' + str(loot_text))
            loserclass = get_database_value(bot, loser, 'class') or 'notclassy'
            ## Barbarians get a 50/50 chance of getting loot even if they lose
            barbarianstealroll = randint(0, 100)
            if loserclass == 'barbarian' and barbarianstealroll >= 50:
                lootwinnermsgb = str(loser + " steals the " + str(loot))
                lootwinner = loser
            elif winner == target:
                lootwinnermsgb = str(winner + " gains the " + str(loot))
                lootwinner = winner
            else:
                lootwinner = winner
            adjust_database_value(bot, lootwinner, loot, defaultadjust)
            if lootwinner == instigator:
                assault_potionswon = assault_potionswon + 1
            else:
                assault_potionslost = assault_potionslost + 1

        ## Magic Attributes text
        magicattributestext = ''
        if instigator != target:
            magicattributestext = get_magic_attributes_text(bot, instigator, target, instigatorshieldstart, targetshieldstart, instigatorcursestart, targetcursestart)

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
            if magicattributestext != '':
                bot.say(str(magicattributestext))
        elif OSDTYPE == 'notice':
            bot.notice(str(announcecombatmsg) + "       " + str(lootwinnermsg), winner)
            bot.notice(str(announcecombatmsg) + "       " + str(lootwinnermsg), loser)
            bot.notice(str(winnermsg)+ "       " + str(lootwinnermsgb), winner)
            bot.notice(str(winnermsg)+ "       " + str(lootwinnermsgb), loser)
            if instigatorpeppernow != instigatorpepperstart or targetpeppernow != targetpepperstart or streaktext:
                bot.notice(str(streaktext) + str(pepperstatuschangemsg), winner)
                bot.notice(str(streaktext) + str(pepperstatuschangemsg), loser)
            if magicattributestext != '':
                bot.notice(str(magicattributestext), winner)
                bot.notice(str(magicattributestext), loser)

        ## update assault stats
        if winner == instigator:
            assault_wins = assault_wins + 1
            assault_damagedealt = assault_damagedealt + int(damage)
            assault_xp = assault_xp + XPearnedwinner
        if loser == instigator:
            assault_losses = assault_losses + 1
            assault_damagetaken = assault_damagetaken + int(damage)
            assault_xp = assault_xp + XPearnedloser

        ## Pause Between duels
        if targetarraytotal > 0 and typeofduel == 'assault':
            bot.notice("  ", instigator)
            time.sleep(5)

        ## End Of assault
        if typeofduel == 'assault':
            set_database_value(bot, target, 'lastfought', targetlastfoughtstart)
            if targetarraytotal == 0:
                bot.notice("  ", instigator)
                bot.notice(instigator + ", It looks like the Full Channel Assault has completed.", instigator)
                for x in assaultstatsarray:
                    workingvar = eval("assault_"+x)
                    if workingvar > 0:
                        newline = str(x + " = " + str(workingvar))
                        if assaultdisplay != '':
                            assaultdisplay = str(assaultdisplay + " " + newline)
                        else:
                            assaultdisplay = str(newline)
                bot.say(instigator + "'s Full Channel Assault results: " + assaultdisplay)

## End Of Duels ###################################################################################################################

## 30 minute automation
@sopel.module.interval(1800)
def halfhourtimer(bot):

    ## bot does not need stats or backpack items
    refreshbot(bot)
    #duelrecorduser
    ## Who gets to win a mysterypotion?
    randomuarray = []
    allusersinroomarray = []
    for u in bot.users:
        allusersinroomarray.append(u)
    duelusersarray = get_database_value(bot, bot.nick, 'duelusers')
    for u in allusersinroomarray:
        ## must have duels enabled
        if u in duelusersarray and u != bot.nick:
            healthcheck(bot, u)
            uclass = get_database_value(bot, u, 'class') or 'notclassy'
            mana = get_database_value(bot, u, 'mana') or 0
            health = get_database_value(bot, u, 'health') or 0


            ## Random user gets a mysterypotion
            lasttimedlootwinner = get_database_value(bot, duelrecorduser, 'lasttimedlootwinner') or bot.nick
            if u != lasttimedlootwinner:
                randomuarray.append(u)

            ## award coin to everyone
            adjust_database_value(bot, u, 'coin', halfhourcoinaward)

            ## colosseum pot
            #adjust_database_value(bot, duelrecorduser, 'colosseum_pot', 5)

            ## health regenerates for all
            if int(health) < healthregenmax:
                adjust_database_value(bot, u, 'health', healthregen)
                health = get_database_value(bot, u, 'health')
                if int(health) > healthregenmax:
                    set_database_value(bot, u, 'health', healthregenmax)

            ## mages regen mana
            if uclass == 'mage':
                if int(mana) < magemanaregenmax:
                    adjust_database_value(bot, u, 'mana', magemanaregen)
                    mana = get_database_value(bot, u, 'mana')
                    if int(mana) > magemanaregenmax:
                        set_database_value(bot, u, 'mana', magemanaregenmax)

    if randomuarray != []:
        lootwinner = halfhourpotionwinner(bot, randomuarray)
        loot_text = get_lootitem_text(bot, lootwinner, 'mysterypotion')
        adjust_database_value(bot, lootwinner, 'mysterypotion', defaultadjust)
        lootwinnermsg = str(lootwinner + ' is awarded a mysterypotion ' + str(loot_text))
        bot.notice(lootwinnermsg, lootwinner)

    ## Clear Last Instigator
    set_database_value(bot, duelrecorduser, 'lastinstigator', None)

    ## bot does not need stats or backpack items
    refreshbot(bot)

## Functions ######################################################################################################################

######################
## Criteria to duel ##
######################

def mustpassthesetoduel(bot, trigger, instigator, target, inchannel, dowedisplay):
    displaymsg = ''
    executedueling = 0
    instigatorlastfought = get_database_value(bot, instigator, 'lastfought') or ''
    instigatortime = get_timesince_duels(bot, instigator, 'timeout') or ''
    targettime = get_timesince_duels(bot, target, 'timeout') or ''
    duelrecordusertime = get_timesince_duels(bot, duelrecorduser, 'timeout') or ''
    duelrecorduserlastinstigator = get_database_value(bot, duelrecorduser, 'lastinstigator') or bot.nick
    dueloptedinarray = get_database_value(bot, bot.nick, 'duelusers') or []
    totalduelusersarray = []
    for u in bot.users:
        if u in dueloptedinarray and u != bot.nick:
            totalduelusersarray.append(u)
    howmanyduelsers = len(totalduelusersarray)

    if not inchannel.startswith("#"):
        displaymsg = str(instigator + " Duels must be in a channel.")
    elif instigator == duelrecorduserlastinstigator and not bot.nick.endswith(devbot):
        displaymsg = str(instigator + ', You may not instigate fights twice in a row within a half hour.')
    elif target == instigatorlastfought and not bot.nick.endswith(devbot) and howmanyduelsers > 2:
        displaymsg = str(instigator + ', You may not fight the same person twice in a row.')
    elif instigator.lower() not in [x.lower() for x in dueloptedinarray]:
        displaymsg = str(instigator + ", It looks like you have disabled duels. Run .duel on to re-enable.")
    elif target.lower() not in [x.lower() for x in dueloptedinarray]:
        displaymsg = str(instigator + ', It looks like ' + target + ' has disabled duels.')
    elif instigatortime <= USERTIMEOUT and not bot.nick.endswith(devbot):
        displaymsg = str("You can't duel for %d seconds." % (USERTIMEOUT - instigatortime))
    elif targettime <= USERTIMEOUT and not bot.nick.endswith(devbot):
        displaymsg = str(target + " can't duel for %d seconds." % (USERTIMEOUT - targettime))
    elif duelrecordusertime <= CHANTIMEOUT and not bot.nick.endswith(devbot):
        displaymsg = str(inchannel + " can't duel for %d seconds." % (CHANTIMEOUT - duelrecordusertime))
    else:
        displaymsg = ''
        executedueling = 1
    if dowedisplay:
        bot.notice(displaymsg, instigator)
    return executedueling

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
    for x in duelstatsadminarray:
        statset = x
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

def whatsyourname(bot, trigger, nick, botownerarray, operatorarray, voicearray, adminsarray):
    nickname = str(nick)

    ## Pepper Level
    pepperstart = get_pepper(bot, nick)

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

    ##  attributes
    nickcurse = get_database_value(bot, nick, 'curse')
    nickshield = get_database_value(bot, nick, 'shield')
    nickcursed = ''
    nickshielded = ''
    if nickcurse or nickshield:
        if nickcurse:
            nickcursed = "(Cursed)"
        if nickshield:
            nickshielded = "(Shielded)"
        nickname = str(nickname + " " + nickcursed + nickshielded)

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
        loot_text = str(loot_text + " Use .duel loot use " + str(loottype) + " to consume.")
    return loot_text

def halfhourpotionwinner(bot, randomuarray):
    winnerselectarray = []
    recentwinnersarray = get_database_value(bot, duelrecorduser, 'lasttimedlootwinners') or []
    lasttimedlootwinner = get_database_value(bot, duelrecorduser, 'lasttimedlootwinner') or bot.nick
    howmanyusers = len(randomuarray)
    if not howmanyusers > 1:
        set_database_value(bot, duelrecorduser, 'lasttimedlootwinner', None)
    for x in randomuarray:
        if x not in recentwinnersarray and x != lasttimedlootwinner:
            winnerselectarray.append(x)
    if winnerselectarray == [] and randomuarray != []:
        set_database_value(bot, duelrecorduser, 'lasttimedlootwinners', None)
        return halfhourpotionwinner(bot, randomuarray)
    lootwinner = get_trigger_arg(winnerselectarray, 'random') or bot.nick
    adjust_database_array(bot, duelrecorduser, lootwinner, 'lasttimedlootwinners', 'add')
    set_database_value(bot, duelrecorduser, 'lasttimedlootwinner', lootwinner)
    return lootwinner

######################
## Weapon Selection ##
######################

## allchan weapons
def getallchanweaponsrandom(bot):
    allchanweaponsarray = []
    for u in bot.users:
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
    howmanyweapons = get_database_array_total(bot, nick, 'weaponslocker') or 0
    if not howmanyweapons > 1:
        set_database_value(bot, nick, 'lastweaponused', None)
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
    elif weapon.lower().startswith(('a ', 'an ', 'the ')):
        weapon = str('with ' + weapon)
    elif weapon.split(' ', 1)[0].endswith("'s"):
        weapon = str('with ' + weapon)
    elif weapon.lower().startswith(('a', 'e', 'i', 'o', 'u')):
        weapon = str('with an ' + weapon)
    elif weapon.lower().startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')):
        if weapon.endswith('s'):
            weapon = str("with " + weapon)
        else:
            weapon = str("with " + weapon + "s")
    elif weapon.lower().startswith('with'):
        weapon = str(weapon)
    else:
        weapon = str('with a ' + weapon)
    return weapon

#################
## Damage Done ##
#################

def damagedone(bot, winner, loser):
    shieldwinner = get_magic_attribute(bot, winner, 'shield')
    shieldloser = get_magic_attribute(bot, loser, 'shield')
    winnerclass = get_database_value(bot, winner, 'class') or 'notclassy'
    loserclass = get_database_value(bot, loser, 'class') or 'notclassy'
    ## Rogue can't be hurt by themselves or bot
    if winner == loser and loserclass == 'rogue':
        damage = 0
    elif winner == bot.nick and loserclass == 'rogue':
        damage = 0
    # magic shield
    elif shieldloser:
        damage = 0
    ## Bot deals a set amount
    elif winner == bot.nick:
        damage = botdamage
    ## Barbarians get extra damage
    elif winnerclass == 'barbarian':
        damage = randint(barbarianminimumdamge, 120)
    else:
        damage = randint(0, 120)
    damage = -abs(damage)
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

def selectwinner(bot, nickarray):
    statcheckarray = ['health','xp','kills','respawns']

    ## empty var to start
    for user in nickarray:
        set_database_value(bot, user, 'winnerselection', None)

    ## everyone gets a roll
    for user in nickarray:
        adjust_database_value(bot, user, 'winnerselection', 1)

    ## random roll
    randomrollwinner = get_trigger_arg(nickarray, 'random')
    adjust_database_value(bot, randomrollwinner, 'winnerselection', 1)

    ## Stats
    for x in statcheckarray:
        statscore = 0
        if x == 'respawns':
            statscore = 99999999
        statleader = ''
        for u in nickarray:
            value = get_database_value(bot, u, x) or 0
            if x == 'respawns':
                if int(value) < statscore:
                    statleader = u
                    statscore = int(value)
            else:
                if int(value) > statscore:
                    statleader = u
                    statscore = int(value)
        adjust_database_value(bot, statleader, 'winnerselection', 1)

    ## weaponslocker not empty
    for user in nickarray:
        weaponslist = get_database_value(bot, user, 'weaponslocker') or []
        if weaponslist != []:
            adjust_database_value(bot, user, 'winnerselection', 1)

    ## anybody rogue?
    for user in nickarray:
        nickclass = get_database_value(bot, user, 'class') or ''
        if nickclass == 'rogue':
            adjust_database_value(bot, user, 'winnerselection', 1)

    ## Dice rolling occurs now
    for user in nickarray:
        rolls = get_database_value(bot, user, 'winnerselection') or 0
        maxroll = winnerdicerolling(bot, user, rolls)
        set_database_value(bot, user, 'winnerselection', maxroll)

    ## curse check
    for user in nickarray:
        curse = get_magic_attribute(bot, user, 'curse')
        if curse:
            set_database_value(bot, user, 'winnerselection', None)

    ## who wins
    winnermax = 0
    winner = ''
    for u in nickarray:
        maxstat = get_database_value(bot, u, 'winnerselection') or 0
        if int(maxstat) > winnermax:
            winner = u
            winnermax = maxstat

    ## Clear value
    for user in nickarray:
        set_database_value(bot, user, 'winnerselection', None)

    return winner

def winnerdicerolling(bot, nick, rolls):
    nickclass = get_database_value(bot, nick, 'class') or ''
    rolla = 0
    rollb = 20
    if nickclass == 'rogue':
        rolla = 10
        rollb = 22
    fightarray = []
    while int(rolls) > 0:
        fightroll = randint(rolla, rollb)
        fightarray.append(fightroll)
        rolls = int(rolls) - 1
    fight = max(fightarray)
    return fight

#####################
## Magic attributes ##
######################

def get_magic_attribute(bot, nick, attribute):
    adjustment = -1
    afflicted = 0
    nickattribute = get_database_value(bot, nick, attribute)
    if nickattribute:
        adjust_database_value(bot, nick, attribute, adjustment)
        afflicted = 1
    return afflicted

def get_current_magic_attributes(bot, instigator, target):
    instigatorshield = get_database_value(bot, instigator, 'shield') or 0
    instigatorcurse = get_database_value(bot, instigator, 'curse') or 0
    targetshield = get_database_value(bot, target, 'shield') or 0
    targetcurse = get_database_value(bot, target, 'curse') or 0
    return instigatorshield, targetshield, instigatorcurse, targetcurse

def get_magic_attributes_text(bot, instigator, target, instigatorshieldstart, targetshieldstart, instigatorcursestart, targetcursestart):
    instigatorshieldnow, targetshieldnow, instigatorcursenow, targetcursenow = get_current_magic_attributes(bot, instigator, target)
    magicattributesarray = ['shield','curse']
    nickarray = ['instigator','target']
    attributetext = ''
    for j in nickarray:
        if j == 'instigator':
            scanningperson = instigator
        else:
            scanningperson = target
        for x in magicattributesarray:
            workingvarnow = eval(j+x+"now")
            workingvarstart = eval(j+x+"start")
            if workingvarnow == 0 and workingvarnow != workingvarstart:
                newline = str(scanningperson + " is no longer affected by " + x + ".")
                if attributetext != '':
                    attributetext = str(attributetext + " " + newline)
                else:
                    attributetext = str(newline)
    return attributetext

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

####################
# Day Of The Week ##
####################

def whatdayofweeknow():
    whatistoday = str(datetime.datetime.today().weekday())
    if whatistoday == '0':
        whatdayofweek = "Monday"
    elif whatistoday == '1':
        whatdayofweek = "Tuesday"
    elif whatistoday == '2':
        whatdayofweek = "Wednesday"
    elif whatistoday == '3':
        whatdayofweek = "Thursday"
    elif whatistoday == '4':
        whatdayofweek = "Friday"
    elif whatistoday == '5':
        whatdayofweek = "Saturday"
    elif whatistoday == '6':
        whatdayofweek = "Sunday"
    return whatistoday, whatdayofweek

##############
## Database ##
##############

def get_database_value(bot, nick, databasekey):
    databasecolumn = str('duels_' + databasekey)
    database_value = bot.db.get_nick_value(nick, databasecolumn) or 0
    return database_value

def set_database_value(bot, nick, databasekey, value):
    databasecolumn = str('duels_' + databasekey)
    bot.db.set_nick_value(nick, databasecolumn, value)

def adjust_database_value(bot, nick, databasekey, value):
    oldvalue = get_database_value(bot, nick, databasekey) or 0
    databasecolumn = str('duels_' + databasekey)
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
        if entry not in adjustarraynew:
            adjustarraynew.append(entry)
    elif adjustmentdirection == 'del':
        if entry in adjustarraynew:
            adjustarraynew.remove(entry)
    for x in adjustarraynew:
        if x not in adjustarray:
            adjustarray.append(x)
    if adjustarray == []:
        set_database_value(bot, nick, databasekey, None)
    else:
        set_database_value(bot, nick, databasekey, adjustarray)

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
            try:
                shuffledarray = random.shuffle(triggerargsarray)
                randomselected = random.randint(0,len(shuffledarray) - 1)
                triggerarg = str(shuffledarray [randomselected])
            except TypeError:
                triggerarg = get_trigger_arg(triggerargsarray, 1)
        else:
            triggerarg = get_trigger_arg(triggerargsarray, 1)
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
