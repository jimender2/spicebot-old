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
from num2words import num2words

## not needed if using without spicebot
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

###################
## Configurables ##
###################

## Timeouts
USERTIMEOUT = 180 ## Time between a users ability to duel - 3 minutes
ROULETTETIMEOUT = 8
CHANTIMEOUT = 40 ## Time between duels in a channel - 40 seconds
OPTTIMEOUT = 1800 ## Time between opting in and out of the game - Half hour
ASSAULTTIMEOUT = 1800 ## Time Between Full Channel Assaults
COLOSSEUMTIMEOUT = 1800 ## Time Between colosseum events
CLASSTIMEOUT = 86400 ## Time between changing class - One Day
INSTIGATORTIMEOUT = 1800
timepotiontargetarray = ['lastinstigator','lastfullroomcolosseuminstigator','lastfullroomassultinstigator']
timepotiontimeoutarray = ['timeout','lastfullroomcolosseum','lastfullroomassult','opttime','classtimeout']

## Half hour timer
scavengercoinaward = 15 ## coin gain per half hour for scavengers
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
lootbuycostscavenger = 80 ## cost to buy a loot item for scavengers
lootbuycost = 100 ## normal cost to buy a loot item
lootsellrewardscavenger = 40 ## coin rewarded in selling loot for scavengers
lootsellreward = 25 ## normal coin rewarded in selling loot
changeclasscost = 100 ## ## how many coin to change class

## Magic usage
magemanamagiccut = .9 ## mages only need 90% of the mana requirements below
manarequiredmagicattack = 250 ## mana required for magic attack
magicattackdamage = -200 ## damage caused by a magic attack
manarequiredmagicshield = 300 ## mana required for magic shield
magicshielddamage = 80 ## damage caused by a magic shield usage
shieldduration = 200 ## how long a shield lasts
manarequiredmagiccurse = 500 ## mana required for magic curse
magiccursedamage = -80 ## damage caused by a magic curse
curseduration = 4 ## how long a curse lasts

## XP points awarded
XPearnedwinnerranger = 7 ## xp earned as a winner and ranger
XPearnedloserranger = 5 ## xp earned as a loser and ranger
XPearnedwinnerstock = 5 ## default xp earned as a winner
XPearnedloserstock = 3 ## default xp earned as a loser

## Class advantages
scavegerfindpercent = 60 ## scavengers have a higher percent chance of finding loot
barbarianminimumdamge = 60 ## Barbarians always strike a set value or above
vampiremaximumdamge = 50

## Bot
botdamage = 150 ## The bot deals a set damage
duelrecorduser = 'duelrecorduser' ## just a database column to store values in
devbot = 'dev' ## If using a development bot and want to bypass commands, this is what the bots name ends in

## other
bugbountycoinaward = 100 ## users that find a bug in the code, get a reward
defaultadjust = 1 ## The default number to increase a stat
GITWIKIURL = "https://github.com/deathbybandaid/SpiceBot/wiki/Duels" ## Wiki URL
grenadefull = 100
grenadesec = 50
weaponmaxlength = 70
randomcoinaward = 100
speceventreward = 500

## Tiers
stockhealth = 1000
stocktierratio = 1
tierratioone = 1.1
tierratiotwo = 1.2
tierratiothree = 1.3
tierratiofour = 1.4
tierratiofive = 1.5
tierratiosix = 1.6
tierratioseven = 1.7
tierratioeight = 1.8
tierrationine = 1.9
tierratioten = 2
tierratioeleven = 2.1
tierratiotwelve = 2.2
tierratiothirteen = 2.3
tierratiofourteen = 2.4
tierratiofifteen = 2.5
tiercommandarray = ['docs','admin','author','on','off','usage','stats','loot','streaks','leaderboard','warroom','weaponslocker','class','magic','random','roulette','assault','colosseum','upupdowndownleftrightleftrightba']
tierunlockdocs, tierunlockadmin, tierunlockauthor, tierunlockon, tierunlockoff, tierunlockusage, tierunlockupupdowndownleftrightleftrightba = 1,1,1,1,1,1,1
tierunlockstats, tierunlockloot, tierunlockstreaks = 2,2,2
tierunlockleaderboard, tierunlockwarroom = 3,3
tierunlockweaponslocker, tierunlockclass, tierunlockmagic = 4,4,4
tierunlockrandom = 5
tierunlockroulette = 6
tierunlockassault = 7
tierunlockcolosseum = 8
tierunlocktitle = 9

## Potion Display Message
healthpotiondispmsg = str(": worth " + str(healthpotionworth) + " health.")
poisonpotiondispmsg = str(": worth " + str(poisonpotionworth) + " health.")
manapotiondispmsg = str(": worth " + str(manapotionworth) + " mana.")
timepotiondispmsg = str(": worth up to " + str(USERTIMEOUT) + " seconds of timeout.")
mysterypotiondispmsg = str(": The label fell off. Use at your own risk!")
magicpotiondispmsg = str(": Not consumable, sellable, or purchasable. Trade this for the potion you want!")

############
## Arrays ##
############

botdevteam = ['deathbybandaid','DoubleD','Mace_Whatdo','dysonparkes','PM','under_score'] ## people to recognize
lootitemsarray = ['healthpotion','manapotion','poisonpotion','timepotion','mysterypotion','magicpotion'] ## types of potions
backpackarray = ['coin','grenade','healthpotion','manapotion','poisonpotion','timepotion','mysterypotion','magicpotion'] ## how to organize backpack
duelstatsarray = ['class','health','curse','shield','mana','xp','wins','losses','winlossratio','respawns','kills','lastfought','timeout']
statsbypassarray = ['winlossratio','timeout'] ## stats that use their own functions to get a value
transactiontypesarray = ['buy','sell','trade','use'] ## valid commands for loot
classarray = ['barbarian','mage','scavenger','rogue','ranger','fiend','vampire','knight','paladin'] ## Valid Classes
duelstatsadminarray = ['levelingtier','weaponslocker','currentlosestreak','magicpotion','currentwinstreak','currentstreaktype','classfreebie','grenade','shield','classtimeout','class','curse','bestwinstreak','worstlosestreak','opttime','coin','wins','losses','health','mana','healthpotion','mysterypotion','timepotion','respawns','xp','kills','timeout','poisonpotion','manapotion','lastfought','konami'] ## admin settings
statsadminchangearray = ['set','reset'] ## valid admin subcommands
magicoptionsarray = ['curse','shield']

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
    dueloptedinarray = get_database_value(bot, bot.nick, 'duelusers') or []
    canduelarray, targetarray = [], []

    ## Time when Module use started
    now = time.time()

    ###### Channel
    inchannel = trigger.sender

    ## bot does not need stats or backpack items
    refreshbot(bot)

    ## Instigator
    instigator = trigger.nick

    ## If Not a target or a command used
    if not fullcommandused:
        bot.notice(instigator + ", Who do you want to duel? Online Docs: " + GITWIKIURL, instigator)

    ## Commands cannot be run if opted out
    elif instigator not in dueloptedinarray and commandortarget.lower() != 'on' and commandortarget.lower() != 'enable' and commandortarget.lower() != 'admin' :
        bot.notice(instigator + ", It looks like you have duels disabled. Run .duel on/enable to enable.", instigator)

    ## Instigator versus Bot
    elif commandortarget == bot.nick:
        bot.say("I refuse to fight a biological entity!")

    ## Instigator versus Instigator
    elif commandortarget == instigator:
        bot.say("If you are feeling self-destructive, there are places you can call.")

    ## Determine if the arg after .duel is a target or a command
    elif commandortarget.lower() not in [u.lower() for u in bot.users]:
        commandortarget = commandortarget.lower()
        
        ## Alternative commands
        if commandortarget == 'enable':
            commandortarget = 'on'
        if commandortarget == 'disable':
            commandortarget = 'off'
        if commandortarget == 'anyone' or commandortarget == 'somebody' or commandortarget == 'available':
            commandortarget = 'random'
        if commandortarget == 'everyone':
            commandortarget = 'assault'
        if commandortarget == 'help':
            commandortarget = 'docs'
        
        ## Tier unlocks
        try:
            commandeval = eval("tierunlock"+ commandortarget) or 0
        except NameError:
            bot.say("This looks like an invalid command or an invalid person.")
            return
        currenttier = get_database_value(bot, duelrecorduser, 'levelingtier') or 0
        if int(commandeval) > int(currenttier) and not bot.nick.endswith(devbot) and commandortarget != 'admin' and commandortarget != 'on':
            tierpepperrequired = get_tierpepper(bot, commandeval)
            tiermath = commandeval - currenttier
            bot.say("Duel "+commandortarget+" will be unlocked when somebody reaches " + str(tierpepperrequired) + ". "+str(tiermath) + " tier(s) remaining!")
            return
        
        ## usage counter
        adjust_database_value(bot, instigator, 'usage', 1)
        
        ## Stat check
        statreset(bot, instigator)
        healthcheck(bot, instigator)
        
        ## Docs
        if commandortarget == 'docs' or commandortarget == 'help':
            target = get_trigger_arg(triggerargsarray, 2)
            if not target:
                bot.say("Online Docs: " + GITWIKIURL)
            elif target.lower() not in [u.lower() for u in bot.users]:
                bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
            else:
                bot.notice("Online Docs: " + GITWIKIURL, target)

        ## Author
        if commandortarget == 'author':
            bot.say("The author of Duels is deathbybandaid.")
        
        ## On/off
        elif commandortarget == 'on' or commandortarget == 'off':
            target = get_trigger_arg(triggerargsarray, 2) or instigator
            targetopttime = get_timesince_duels(bot, target, 'opttime')
            if target.lower() not in [u.lower() for u in bot.users] and target != 'everyone':
                bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
            elif target != instigator and not trigger.admin:
                bot.notice(instigator + "This is an admin only function.", instigator)
            elif target == 'everyone':
                for u in bot.users:
                    if commandortarget == 'on':
                        adjust_database_array(bot, bot.nick, target, 'duelusers', 'add')
                    else:
                        adjust_database_array(bot, bot.nick, target, 'duelusers', 'del')
                bot.notice(instigator + ", duels should now be " +  commandortarget + ' for ' + target + '.', instigator)
            elif targetopttime < OPTTIMEOUT and not trigger.admin and not bot.nick.endswith(devbot):
                bot.notice(instigator + " It looks like " + target + " can't enable/disable duels for " + str(hours_minutes_seconds((OPTTIMEOUT - targetopttime))), instigator)
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

        ## Russian Roulette
        elif commandortarget == 'roulette':
            if not inchannel.startswith("#"):
                bot.notice(instigator + " Duels must be in channel.", instigator)
                return
            getlastusage = get_timesince_duels(bot, duelrecorduser, str('lastfullroom' + commandortarget)) or ROULETTETIMEOUT
            if getlastusage < ROULETTETIMEOUT and not bot.nick.endswith(devbot):
                bot.notice(instigator + " Roulette has a small timeout.", instigator)
                return
            set_database_value(bot, duelrecorduser, str('lastfullroom' + commandortarget), now)
            roulettepayoutdefault = 5
            roulettelastplayer = get_database_value(bot, duelrecorduser, 'roulettelastplayer') or bot.nick
            roulettecount = get_database_value(bot, duelrecorduser, 'roulettecount') or 1
            if roulettelastplayer == instigator:
                bot.say(instigator + " spins the revolver and pulls the trigger.")
            else:
                bot.say(instigator + " spins the cylinder and pulls the trigger.")
            roulettechamber = get_database_value(bot, duelrecorduser, 'roulettechamber')
            if not roulettechamber:
                roulettechamber = randint(1, 6)
                set_database_value(bot, duelrecorduser, 'roulettechamber', roulettechamber)
            roulettespinarray = get_database_value(bot, duelrecorduser, 'roulettespinarray') or [1,2,3,4,5,6]
            if roulettelastplayer == instigator:
                if len(roulettespinarray) > 1:
                    temparray = []
                    for x in roulettespinarray:
                        if x != roulettechamber:
                            temparray.append(x)
                    randomremove = get_trigger_arg(temparray, "random")
                    roulettespinarray.remove(randomremove)
                    currentspin = get_trigger_arg(roulettespinarray, "random")
                    set_database_value(bot, duelrecorduser, 'roulettespinarray', roulettespinarray)
                else:
                    currentspin = roulettechamber
                    set_database_value(bot, duelrecorduser, 'roulettespinarray', None)
            else:
                set_database_value(bot, duelrecorduser, 'roulettespinarray', None)
            currentspin = get_trigger_arg(roulettespinarray, "random")
            if currentspin == roulettechamber:
                biggestpayout = 0
                biggestpayoutwinner = ''
                statreset(bot, instigator)
                healthcheck(bot, instigator)
                roulettewinners = get_database_value(bot, duelrecorduser, 'roulettewinners') or []
                resultmsg = ''
                deathmsg = ''
                revolvernames = ['.357 Magnum','Colt PeaceMaker','Colt Repeater','Colt Single Action Army 45','Ruger Super Blackhawk','Remington Model 1875','Russian Nagant M1895 revolver','Smith and Wesson Model 27']
                weapon = get_trigger_arg(revolvernames, 'random')
                weapon = str(" with a " + weapon)
                winner, loser = 'duelsroulettegame', instigator
                damage, roulettedamage = damagedone(bot, winner, loser, weapon, 1)
                currenthealth = get_database_value(bot, loser, 'health')
                if currenthealth <= 0:
                    whokilledwhom(bot, bot.nick, loser)
                    deathmsg = str(" " +  loser + ' dies forcing a respawn!!')
                if roulettecount == 1:
                    resultmsg = "First in the chamber. What bad luck. "
                    roulettewinners.append(instigator)
                resultmsg = str(resultmsg + roulettedamage + deathmsg)
                uniqueplayersarray = []
                for x in roulettewinners:
                    if x not in uniqueplayersarray:
                        uniqueplayersarray.append(x)
                for x in uniqueplayersarray:
                    if x != instigator:
                        statreset(bot, x)
                        healthcheck(bot, x)
                        roulettepayoutx = get_database_value(bot, x, 'roulettepayout')
                        if roulettepayoutx > biggestpayout:
                            biggestpayoutwinner = x
                            biggestpayout = roulettepayoutx
                        if roulettepayoutx == biggestpayout:
                            biggestpayoutwinner = str(biggestpayoutwinner+ " " + x)
                            biggestpayout = roulettepayoutx
                        adjust_database_value(bot, x, 'coin', roulettepayoutx)
                        bot.notice(x + ", your roulette payouts = " + str(roulettepayoutx) + " coins!", x)
                    set_database_value(bot, x, 'roulettepayout', None)
                if instigator in roulettewinners:
                    roulettewinners.remove(instigator)
                if roulettewinners != []:
                    displaymessage = get_trigger_arg(roulettewinners, "list")
                    displaymessage = str("Winners: " + displaymessage + " ")
                if biggestpayoutwinner != '':
                    displaymessage = str(displaymessage +"     Biggest Payout: "+ biggestpayoutwinner + " with " + str(biggestpayout) + " coins. ")
                set_database_value(bot, duelrecorduser, 'roulettelastplayer', None)
                set_database_value(bot, duelrecorduser, 'roulettechamber', None)
                set_database_value(bot, duelrecorduser, 'roulettewinners', None)
                roulettecount = get_database_value(bot, duelrecorduser, 'roulettecount') or 1
                set_database_value(bot, duelrecorduser, 'roulettecount', None)
                if roulettecount > 1:
                    displaymessage = str(displaymessage +"     The chamber spun " + str(roulettecount) + " times. ")
                bot.say(resultmsg + displaymessage)
            else:
                bot.say("*click*")
                roulettecount = roulettecount + 1
                roulettepayout = roulettepayoutdefault * roulettecount
                adjust_database_value(bot, instigator, 'roulettepayout', roulettepayout)
                adjust_database_value(bot, duelrecorduser, 'roulettecount', defaultadjust)
                set_database_value(bot, duelrecorduser, 'roulettelastplayer', instigator)
                adjust_database_array(bot, duelrecorduser, instigator, 'roulettewinners', 'add')

        ## Usage
        elif commandortarget == 'usage':
            target = get_trigger_arg(triggerargsarray, 2) or instigator
            targetname = target
            if target == 'channel':
                target = duelrecorduser
            totaluses = get_database_value(bot, target, 'usage')
            bot.say(targetname + " has used duels " + str(totaluses) + " times.")
            
        ## Colosseum, Assault, and Random
        elif commandortarget == 'colosseum' or commandortarget == 'assault' or commandortarget == 'random':
            if not inchannel.startswith("#"):
                bot.notice(instigator + " Duels must be in channel.", instigator)
                return
            for u in bot.users:
                canduel = mustpassthesetoduel(bot, trigger, u, u, dowedisplay)
                if canduel:
                    canduelarray.append(u)
            if commandortarget != 'random' and bot.nick in canduelarray:
                canduelarray.remove(bot.nick)
            if canduelarray == [] or len(canduelarray) == 1:
                bot.notice(instigator + ", It looks like the full channel " + commandortarget + " event target finder has failed.", instigator)
                return
            if commandortarget == 'random':
                typeofduel == 'random'
                target = get_trigger_arg(canduelarray, 'random')
                OSDTYPE = 'say'
                targetarray.append(target)
                getreadytorumble(bot, trigger, instigator, targetarray, OSDTYPE, fullcommandused, now, triggerargsarray, typeofduel, inchannel)
                return
            timeouteval = eval(commandortarget.upper() + "TIMEOUT")
            getlastusage = get_timesince_duels(bot, duelrecorduser, str('lastfullroom' + commandortarget)) or timeouteval
            getlastinstigator = get_database_value(bot, duelrecorduser, str('lastfullroom' + commandortarget + 'instigator')) or bot.nick
            if getlastusage < timeouteval and not bot.nick.endswith(devbot):
                bot.notice(instigator + ", full channel " + commandortarget + " event can't be used for "+str(hours_minutes_seconds((timeouteval - getlastusage)))+".", instigator)
            elif getlastinstigator == instigator and not bot.nick.endswith(devbot):
                bot.notice(instigator + ", You may not instigate a full channel " + commandortarget + " event twice in a row.", instigator)
            elif instigator not in canduelarray:
                dowedisplay = 1
                mustpassthesetoduel(bot, trigger, instigator, instigator, dowedisplay)
            else:
                if instigator in canduelarray and commandortarget == 'assault':
                    canduelarray.remove(instigator)
                displaymessage = get_trigger_arg(canduelarray, "list")
                bot.say(instigator + " Initiated a full channel " + commandortarget + " event. Good luck to " + displaymessage)
                set_database_value(bot, duelrecorduser, str('lastfullroom' + commandortarget), now)
                set_database_value(bot, duelrecorduser, str('lastfullroom' + commandortarget + 'instigator'), instigator)
                if commandortarget == 'assault':
                    OSDTYPE = 'notice'
                    lastfoughtstart = get_database_value(bot, instigator, 'lastfought')
                    typeofduel = 'assault'
                    getreadytorumble(bot, trigger, instigator, canduelarray, OSDTYPE, fullcommandused, now, triggerargsarray, typeofduel, inchannel)
                    set_database_value(bot, instigator, 'lastfought', lastfoughtstart)
                elif commandortarget == 'colosseum':
                    statreset(bot, instigator)
                    healthcheck(bot, instigator)
                    totalplayers = len(canduelarray)
                    riskcoins = int(totalplayers) * 30
                    damage = riskcoins
                    winner = selectwinner(bot, canduelarray)
                    bot.say("The Winner is: " + winner + "! Total winnings: " + str(riskcoins) + " coin! Losers took " + str(riskcoins) + " damage.")
                    diedinbattle = []
                    canduelarray.remove(winner)
                    for x in canduelarray:
                        statreset(bot, x)
                        healthcheck(bot, x)
                        shieldloser = get_database_value(bot, x, 'shield') or 0
                        if shieldloser and damage > 0:
                            damagemath = int(shieldloser) - damage
                            if int(damagemath) > 0:
                                adjust_database_value(bot, x, 'shield', -abs(damage))
                                damage = 0
                            else:
                                damage = abs(damagemath)
                                set_database_value(bot, x, 'shield', None)
                        if damage > 0:
                            adjust_database_value(bot, x, 'health', -abs(damage))
                            currenthealth = get_database_value(bot, x, 'health')
                        if currenthealth <= 0:
                            whokilledwhom(bot, winner, x)
                            diedinbattle.append(x)
                    displaymessage = get_trigger_arg(diedinbattle, "list")
                    if displaymessage:
                        bot.say(displaymessage + " died in this event.")
                    adjust_database_value(bot, winner, 'coin', riskcoins)

        ## War Room
        elif commandortarget == 'warroom':
            subcommand = get_trigger_arg(triggerargsarray, 2).lower()
            for u in bot.users:
                canduel = mustpassthesetoduel(bot, trigger, u, u, dowedisplay)
                if canduel and u != bot.nick:
                    canduelarray.append(u)
            if not subcommand:
                if instigator in canduelarray:
                    bot.notice(instigator + ", It looks like you can duel.", instigator)
                else:
                    dowedisplay = 1
                    mustpassthesetoduel(bot, trigger, instigator, instigator, dowedisplay)
            elif subcommand == 'colosseum' or subcommand == 'assault':
                if subcommand == 'everyone':
                    subcommand = 'assault'
                timeouteval = eval(subcommand.upper() + "TIMEOUT")
                getlastusage = get_timesince_duels(bot, duelrecorduser, str('lastfullroom' + subcommand)) or timeouteval
                getlastinstigator = get_database_value(bot, duelrecorduser, str('lastfullroom' + subcommand + 'instigator')) or bot.nick
                if getlastinstigator == instigator and not bot.nick.endswith(devbot):
                    bot.notice(instigator + ", You may not instigate a full channel " + subcommand + " event twice in a row.", instigator)
                elif getlastusage < timeouteval and not bot.nick.endswith(devbot):
                    bot.notice(instigator + ", full channel " + subcommand + " event can't be used for "+str(hours_minutes_seconds((timeouteval - getlastusage)))+".", instigator)
                else:
                    bot.notice(instigator + ", It looks like full channel " + subcommand + " event can be used.", instigator)
            elif subcommand == 'list':
                if instigator in canduelarray:
                    canduelarray.remove(instigator)
                displaymessage = get_trigger_arg(canduelarray, "list")
                bot.say(instigator + ", you may duel the following users: "+ str(displaymessage ))
            elif subcommand.lower() not in [u.lower() for u in bot.users]:
                bot.notice(instigator + ", It looks like " + str(subcommand) + " is either not here, or not a valid person.", instigator)
            else:
                if subcommand in canduelarray:
                    bot.notice(instigator + ", It looks like you can duel " + subcommand + ".", instigator)
                else:
                    dowedisplay = 1
                    mustpassthesetoduel(bot, trigger, instigator, subcommand, dowedisplay)

        ## Title
        elif commandortarget == 'title':
            instigatortitle = get_database_value(bot, instigator, 'title')
            titletoset = get_trigger_arg(triggerargsarray, 2)
            if not titletoset:
                unsetmsg = ''
                if not instigatortitle:
                    unsetmsg = "You don't have a title! "
                bot.say(unsetmsg + "What do you want your title to be?")
            elif titletoset == 'remove':
                set_database_value(bot, instigator, 'title', None)
            else:
                instigatorcoin = get_database_value(bot, instigator, 'coin') or 0
                if instigatorcoin < changeclasscost:
                    bot.say("Changing your title costs " + str(changeclasscost) + " coin. You need more funding.")
                elif len() > 10:
                    bot.say("Purchased titles can be no longer than 10 characters")
                else:
                    set_database_value(bot, instigator, 'title', titletoset)
            
        ## Class
        elif commandortarget == 'class':
            subcommandarray = ['set','change']
            classes = get_trigger_arg(classarray, "list")
            subcommand = get_trigger_arg(triggerargsarray, 2).lower()
            setclass = get_trigger_arg(triggerargsarray, 3).lower()
            instigatorclass = get_database_value(bot, instigator, 'class')
            instigatorfreebie = get_database_value(bot, instigator, 'classfreebie') or 0
            classtime = get_timesince_duels(bot, instigator, 'classtimeout')
            instigatorclasstime = get_timesince_duels(bot, instigator, 'classtimeout')
            instigatorcoin = get_database_value(bot, instigator, 'coin') or 0
            if not instigatorclass and not subcommand:
                bot.say("You don't appear to have a class set. Options are : " + classes + ". Run .duel class set    to set your class.")
            elif not subcommand:
                bot.say("Your class is currently set to " + str(instigatorclass) + ". Use .duel class change    to change class. Options are : " + classes + ".")
            elif classtime < CLASSTIMEOUT and not bot.nick.endswith(devbot):
                bot.say("You may not change your class more than once per 24 hours. Please wait "+str(hours_minutes_seconds((CLASSTIMEOUT - instigatorclasstime)))+" to change.")
            elif subcommand not in subcommandarray:
                bot.say("Invalid command. Options are set or change.")
            elif not setclass:
                bot.say("Which class would you like to use? Options are: " + classes +".")
            elif instigatorcoin < changeclasscost and instigatorfreebie:
                bot.say("Changing class costs " + str(changeclasscost) + " coin. You need more funding.")
            elif setclass not in classarray:
                bot.say("Invalid class. Options are: " + classes +".")
            elif setclass == instigatorclass:
                bot.say('Your class is already set to ' +  setclass)
            else:
                statreset(bot, instigator)
                healthcheck(bot, instigator)
                set_database_value(bot, instigator, 'class', setclass)
                bot.say('Your class is now set to ' +  setclass)
                set_database_value(bot, instigator, 'classtimeout', now)
                if instigatorfreebie:
                    adjust_database_value(bot, instigator, 'coin', -abs(changeclasscost))
                else:
                    set_database_value(bot, instigator, 'classfreebie', 1)

        ## Streaks
        elif commandortarget == 'streaks':
            target = get_trigger_arg(triggerargsarray, 2) or instigator
            if target.lower() not in [u.lower() for u in bot.users]:
                bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
            elif target.lower() not in [x.lower() for x in dueloptedinarray]:
                bot.notice(instigator + ", It looks like " + target + " has duels off.", instigator)
            else:
                healthcheck(bot, target)
                statreset(bot, target)
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

        ## Stats
        elif commandortarget == 'stats':
            target = get_trigger_arg(triggerargsarray, 2) or instigator
            if target.lower() not in [u.lower() for u in bot.users]:
                bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
            elif target.lower() not in [x.lower() for x in dueloptedinarray]:
                bot.notice(instigator + ", It looks like " + target + " has duels off.", instigator)
            else:
                #healthcheck(bot, target)
                statreset(bot, target)
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
                    if not pepper or pepper == '':
                        targetname = target
                    else:
                        targetname = str("(" + str(pepper) + ") " + target)
                    displaymessage = str(targetname + "'s " + commandortarget + ":" + displaymessage)
                    bot.say(displaymessage)
                else:
                    bot.say(instigator + ", It looks like " + target + " has no " +  commandortarget + ".", instigator)

        ## Leaderboard
        elif commandortarget == 'leaderboard':
            subcommand = get_trigger_arg(triggerargsarray, 2)
            if not subcommand:
                leaderscript = []
                leaderboardarraystats = ['winlossratio','kills','respawns','health','bestwinstreak','worstlosestreak']
                worstlosestreakdispmsg, worstlosestreakdispmsgb = "Worst Losing Streak:", ""
                winlossratiodispmsg, winlossratiodispmsgb = "Wins/Losses:", ""
                killsdispmsg, killsdispmsgb = "Most Kills:", "kills"
                respawnsdispmsg, respawnsdispmsgb = "Most Deaths:", "respawns"
                healthdispmsg, healthdispmsgb = "Closest To Death:", "health"
                bestwinstreakdispmsg, bestwinstreakdispmsgb = "Best Win Streak:", ""
                for x in leaderboardarraystats:
                    statleadername = ''
                    if x != 'health':
                        statleadernumber = 0
                    else:
                        statleadernumber = 99999999
                    for u in bot.users:
                        #healthcheck(bot, u)
                        statreset(bot, u)
                        if u in dueloptedinarray:
                            if x != 'winlossratio':
                                statamount = get_database_value(bot, u, x)
                            else:
                                scriptdef = str('get_' + x + '(bot,u)')
                                statamount = eval(scriptdef)
                            if statamount == statleadernumber and statamount > 0:
                                statleadername = str(statleadername+ " "+ u)
                            else:
                                if x != 'health':
                                    if statamount > statleadernumber:
                                        statleadernumber = statamount
                                        statleadername = u
                                else:
                                    if statamount < statleadernumber and statamount > 0:
                                        statleadernumber = statamount
                                        statleadername = u
                    if x == 'winlossratio':
                        statleadernumber = format(statleadernumber, '.3f')
                    if statleadername != '':
                        msgtoadd = str(eval(x+"dispmsg") + " "+ statleadername + " at "+ str(statleadernumber)+ " "+ eval(x+"dispmsgb"))
                        leaderscript.append(msgtoadd)
                if leaderscript == []:
                    displaymessage = str("Leaderboard appears to be empty")
                else:
                    for msg in leaderscript:
                        displaymessage = str(displaymessage+ msg+ "  ")
                bot.say(displaymessage)
            if subcommand == 'highest' or subcommand == 'lowest':
                subcommanda = get_trigger_arg(triggerargsarray, 3)
                if not subcommanda:
                    bot.say("What stat do you want to check highest/losest?")
                elif subcommanda not in duelstatsadminarray and subcommanda != 'class':
                    bot.say("This stat is either not comparable at the moment or invalid.")
                else:
                    statleadername = ''
                    if subcommand == 'highest':
                        statleadernumber = 0
                    else:
                        statleadernumber = 99999999
                    for u in bot.users:
                        if subcommanda != 'winlossratio':
                            statamount = get_database_value(bot, u, subcommanda)
                        else:
                            scriptdef = str('get_' + subcommanda + '(bot,u)')
                            statamount = eval(scriptdef)
                        if statamount == statleadernumber and statamount > 0:
                            statleadername = str(statleadername+ " "+ u)
                        else:
                            if subcommand == 'highest':
                                if statamount > statleadernumber:
                                    statleadernumber = statamount
                                    statleadername = u
                            else:
                                if statamount < statleadernumber and statamount > 0:
                                    statleadernumber = statamount
                                    statleadername = u
                    if statleadername != '':
                        bot.say("The " + subcommand + " amount for "+ subcommanda+ " is " + statleadername+ " with "+ str(statleadernumber))
                    else:
                        bot.say("There doesn't appear to be a "+ subcommand + " amount for "+subcommanda+".")

        ## Loot Items
        elif commandortarget == 'loot':
            instigatorclass = get_database_value(bot, instigator, 'class')
            instigatorcoin = get_database_value(bot, instigator, 'coin') or 0
            lootcommand = get_trigger_arg(triggerargsarray, 2).lower()
            if not lootcommand or lootcommand.lower() in [x.lower() for x in dueloptedinarray]:
                target = get_trigger_arg(triggerargsarray, 2) or instigator
                if target.lower() not in [u.lower() for u in bot.users]:
                    bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
                else:
                    statreset(bot, target)
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
            elif lootcommand not in transactiontypesarray:
                transactiontypesarraylist = get_trigger_arg(transactiontypesarray, "list")
                bot.notice(instigator + ", It looks like " + lootcommand + " is either not here, not a valid person, or an invalid command. Valid commands are: " + transactiontypesarraylist, instigator)
            elif lootcommand == 'use':
                lootitem = get_trigger_arg(triggerargsarray, 3).lower()
                gethowmanylootitem = get_database_value(bot, instigator, lootitem) or 0
                if not lootitem:
                    bot.notice(instigator + ", What do you want to " + str(lootcommand) + "?", instigator)
                elif lootitem not in lootitemsarray and lootitem != 'grenade':
                    bot.notice(instigator + ", Invalid loot item.", instigator)
                elif not gethowmanylootitem:
                    bot.notice(instigator + ", You do not have any " +  lootitem + "!", instigator)
                elif lootitem == 'magicpotion':
                    bot.say("Magic Potions are not purchasable, sellable, or usable. They can only be traded.")
                elif lootitem == 'grenade':
                    if not inchannel.startswith("#"):
                        bot.notice(instigator + ", grenades must be used in channel.", instigator)
                        return
                    instigatorgrenade = get_database_value(bot, instigator, 'grenade') or 0
                    for u in bot.users:
                        if u in dueloptedinarray and u != bot.nick and u != instigator:
                            canduelarray.append(u)
                            statreset(bot, target)
                            healthcheck(bot, u)
                    if canduelarray == []:
                        bot.notice(instigator + ", It looks like using a grenade right now won't hurt anybody.", instigator)
                    else:
                        canduelarrayorig = []
                        for u in canduelarray:
                            canduelarrayorig.append(u)
                            targethealth = get_database_value(bot, u, 'health')
                        adjust_database_value(bot, instigator, lootitem, -1)
                        fulltarget, secondarytarget, thirdtarget = '','',''
                        fulltarget = get_trigger_arg(canduelarray, "random")
                        displaymsg = str(fulltarget + " takes the brunt of the grenade dealing " + str(abs(grenadefull)) + " damage. ")
                        canduelarray.remove(fulltarget)
                        if canduelarray != []:
                            secondarytarget = get_trigger_arg(canduelarray, "random")
                            canduelarray.remove(secondarytarget)
                            if canduelarray != []:
                                thirdtarget = get_trigger_arg(canduelarray, "random")
                                displaymsg = str(displaymsg + secondarytarget + " and " + thirdtarget + " jump away but still take " + str(abs(grenadesec)) + " damage. ")
                                canduelarray.remove(thirdtarget)
                                if canduelarray != []:
                                    remainingarray = get_trigger_arg(canduelarray, "list")
                                    displaymsg = str(displaymsg + remainingarray + " completely jump out of the way")
                            else:
                                displaymsg = str(displaymsg + secondarytarget + " jumps away but still takes " + str(abs(grenadesec)) + " damage. ")
                        painarray = []
                        damagearray = []
                        deatharray = []
                        if fulltarget != '':
                            painarray.append(fulltarget)
                            damagearray.append(grenadefull)
                        if secondarytarget != '':
                            painarray.append(secondarytarget)
                            damagearray.append(grenadesec)
                        if thirdtarget != '':
                            painarray.append(thirdtarget)
                            damagearray.append(grenadesec)
                        for x, damage in zip(painarray, damagearray):
                            damage = int(damage)
                            shieldloser = get_database_value(bot, x, 'shield') or 0
                            if shieldloser and damage > 0:
                                damagemath = int(shieldloser) - damage
                                if int(damagemath) > 0:
                                    adjust_database_value(bot, x, 'shield', -abs(damage))
                                    damage = 0
                                else:
                                    damage = abs(damagemath)
                                    set_database_value(bot, x, 'shield', None)
                            if damage > 0:
                                adjust_database_value(bot, x, 'health', -abs(damage))
                            xhealth = get_database_value(bot, x, 'health') or 0
                            if int(xhealth) <= 0:
                                whokilledwhom(bot, instigator, x)
                                deatharray.append(x)
                        if deatharray != []:
                            deadarray = get_trigger_arg(deatharray, "list")
                            displaymsg = str(displaymsg + "    " + deadarray + " died by this grenade volley")
                        if displaymsg != '':
                            bot.say(displaymsg)
                else:
                    targnum = get_trigger_arg(triggerargsarray, 4).lower()
                    if not targnum:
                        quantity = 1
                        target = instigator
                    elif targnum.isdigit():
                        quantity = int(targnum)
                        target = instigator
                    elif targnum.lower() in [x.lower() for x in dueloptedinarray]:
                        targnumb = get_trigger_arg(triggerargsarray, 5).lower()
                        target = targnum
                        if not targnumb:
                            quantity = 1
                        elif targnumb.isdigit():
                            quantity = int(targnumb)
                        elif targnumb == 'all':
                            quantity = int(gethowmanylootitem)
                        else:
                            bot.say("Invalid command.")
                            return
                    elif targnum == 'all':
                        target = instigator
                        quantity = int(gethowmanylootitem)
                    elif target.lower() not in [x.lower() for x in dueloptedinarray]:
                        bot.notice(instigator + ", It looks like " + target + " has duels off.", instigator)
                    elif target.lower() not in [u.lower() for u in bot.users]:
                        bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
                    else:
                        bot.say("Invalid command.")
                        return
                    targetclass = get_database_value(bot, target, 'class') or 'notclassy'
                    if int(gethowmanylootitem) < int(quantity):
                        bot.notice(instigator + ", You do not have enough " +  lootitem + " to use this command!", instigator)
                    elif target == bot.nick:
                        bot.notice(instigator + ", I am immune to " + lootitem, instigator)
                    elif target.lower() != instigator.lower() and targetclass == 'fiend':
                        bot.notice(instigator + ", It looks like " + target + " is a fiend and can only self-use potions.", instigator)
                        adjust_database_value(bot, instigator, lootitem, -abs(quantity))
                    else:
                        uselootarray = []
                        adjust_database_value(bot, instigator, lootitem, -abs(quantity))
                        lootusedeaths = 0
                        if lootitem == 'mysterypotion':
                            while int(quantity) > 0:
                                quantity = quantity - 1
                                loot = get_trigger_arg(lootitemsarray, 'random')
                                if loot == 'mysterypotion' or loot == 'magicpotion':
                                    nulllootitemsarray = ['water','vinegar','mud']
                                    loot = get_trigger_arg(nulllootitemsarray, 'random')
                                uselootarray.append(loot)
                        else:
                            while int(quantity) > 0:
                                quantity = quantity - 1
                                uselootarray.append(lootitem)
                        uselootarraytotal = len(uselootarray)
                        if target == instigator:
                            if int(uselootarraytotal) == 1:
                                mainlootusemessage = str(instigator + ' uses ' + lootitem + '.')
                            else:
                                mainlootusemessage = str(instigator + ' uses ' + str(uselootarraytotal) + " " + lootitem + 's.')
                        else:
                            if int(uselootarraytotal) == 1:
                                mainlootusemessage = str(instigator + ' uses ' + lootitem + ' on ' + target + ".")
                            else:
                                mainlootusemessage = str(instigator + " used " + str(uselootarraytotal) + " " + lootitem + "s on " + target +".")
                        for x in uselootarray:
                            if x == 'healthpotion':
                                if targetclass == 'barbarian':
                                    adjust_database_value(bot, target, 'health', healthpotionworthbarbarian)
                                else:
                                    adjust_database_value(bot, target, 'health', healthpotionworth)
                            elif x == 'poisonpotion':
                                adjust_database_value(bot, target, 'health', poisonpotionworth)
                            elif x == 'manapotion':
                                if targetclass == 'mage':
                                    adjust_database_value(bot, target, 'mana', manapotionworthmage)
                                else:
                                    adjust_database_value(bot, target, 'mana', manapotionworth)
                            elif x == 'timepotion':
                                set_database_value(bot, target, 'lastfought', None)
                                for k in timepotiontargetarray:
                                    targetequalcheck = get_database_value(bot, duelrecorduser, k) or bot.nick
                                    if targetequalcheck == target:
                                        set_database_value(bot, duelrecorduser, k, None)
                                for j in timepotiontimeoutarray:
                                    set_database_value(bot, target, k, None)
                                set_database_value(bot, duelrecorduser, 'timeout', None)
                            targethealth = get_database_value(bot, target, 'health')
                            if targethealth <= 0:
                                lootusedeaths = lootusedeaths + 1
                                whokilledwhom(bot, instigator, target)
                        if lootitem == 'mysterypotion':
                            postionsusedarray = get_trigger_arg(uselootarray, "list")
                            mainlootusemessage = str(mainlootusemessage + " Potions used: " + postionsusedarray)
                        if lootusedeaths > 0:
                            if lootusedeaths == 1:
                                mainlootusemessage = str(mainlootusemessage + " This resulted in death.")
                            else:
                                mainlootusemessage = str(mainlootusemessage + " This resulted in "+str(lootusedeaths)+" deaths.")
                        bot.say(mainlootusemessage)
                        if target != instigator and not inchannel.startswith("#"):
                            bot.notice(mainlootusemessage, target)
            elif lootcommand == 'buy':
                lootitem = get_trigger_arg(triggerargsarray, 3).lower()
                if not lootitem:
                    bot.notice(instigator + ", What do you want to " + str(lootcommand) + "?", instigator)
                elif lootitem not in lootitemsarray:
                    bot.notice(instigator + ", Invalid loot item.", instigator)
                elif lootitem == 'magicpotion':
                    bot.say("Magic Potions are not purchasable, sellable, or usable. They can only be traded.")
                else:
                    quantity = get_trigger_arg(triggerargsarray, 4).lower() or 1
                    if quantity == 'all':
                        if instigatorclass == 'scavenger':
                            quantity = int(instigatorcoin) / lootbuycostscavenger
                        else:
                            quantity = int(instigatorcoin) / lootbuycostscavenger
                        if not quantity > 1:
                            bot.notice(instigator + ", You do not have enough coin for this action.", instigator)
                            return
                    quantity = int(quantity)
                    if instigatorclass == 'scavenger':
                        coinrequired = lootbuycostscavenger * int(quantity)
                    else:
                        coinrequired = lootbuycost * int(quantity)
                    if instigatorcoin < coinrequired:
                        bot.notice(instigator + ", You do not have enough coin for this action.", instigator)
                    else:
                        adjust_database_value(bot, instigator, 'coin', -abs(coinrequired))
                        adjust_database_value(bot, instigator, lootitem, quantity)
                        bot.say(instigator + " bought " + str(quantity) +  " "+lootitem + "s for " +str(coinrequired)+ " coins.")
            elif lootcommand == 'sell':
                lootitem = get_trigger_arg(triggerargsarray, 3).lower()
                gethowmanylootitem = get_database_value(bot, instigator, lootitem) or 0
                if not lootitem:
                    bot.notice(instigator + ", What do you want to " + str(lootcommand) + "?", instigator)
                elif lootitem not in lootitemsarray:
                    bot.notice(instigator + ", Invalid loot item.", instigator)
                elif not gethowmanylootitem:
                    bot.notice(instigator + ", You do not have any " +  lootitem + "!", instigator)
                elif lootitem == 'magicpotion':
                    bot.say("Magic Potions are not purchasable, sellable, or usable. They can only be traded.")
                else:
                    quantity = get_trigger_arg(triggerargsarray, 4).lower() or 1
                    if quantity == 'all':
                        quantity = gethowmanylootitem
                    if int(quantity) > gethowmanylootitem:
                        bot.notice(instigator + ", You do not have enough " + lootitem + " for this action.", instigator)
                    else:
                        quantity = int(quantity)
                        if instigatorclass == 'scavenger':
                            reward = lootsellrewardscavenger * int(quantity)
                        else:
                            reward = lootsellreward * int(quantity)
                        adjust_database_value(bot, instigator, 'coin', reward)
                        adjust_database_value(bot, instigator, lootitem, -abs(quantity))
                        bot.say(instigator + " sold " + str(quantity) + " "+ lootitem + "s for " +str(reward)+ " coins.")
            elif lootcommand == 'trade':
                lootitem = get_trigger_arg(triggerargsarray, 3).lower()
                lootitemb = get_trigger_arg(triggerargsarray, 4).lower()
                if not lootitem or not lootitemb:
                    bot.notice(instigator + ", What do you want to " + str(lootcommand) + "?", instigator)
                elif lootitem not in lootitemsarray or lootitemb not in lootitemsarray:
                    bot.notice(instigator + ", Invalid loot item.", instigator)
                if lootitem == 'grenade' or lootitemb == 'grenade':
                    bot.notice(instigator + ", You can't trade for grenades.", instigator)
                elif lootitemb == lootitem:
                    bot.notice(instigator + ", You can't trade for the same type of potion.", instigator)
                else:
                    gethowmanylootitem = get_database_value(bot, instigator, lootitem) or 0
                    quantity = get_trigger_arg(triggerargsarray, 5).lower() or 1
                    if lootitem == 'magicpotion':
                        tradingratio = 1
                    elif instigatorclass == 'scavenger':
                        tradingratio = traderatioscavenger
                    else:
                        tradingratio = traderatio
                    if quantity == 'all':
                        quantity = gethowmanylootitem / tradingratio
                    if quantity < 0:
                        bot.notice(instigator + ", You do not have enough "+lootitem+" for this action.", instigator)
                        return
                    quantitymath = tradingratio * int(quantity)
                    if gethowmanylootitem < quantitymath:
                        bot.notice(instigator + ", You don't have enough of this item to trade.", instigator)
                    else:
                        adjust_database_value(bot, instigator, lootitem, -abs(quantitymath))
                        adjust_database_value(bot, instigator, lootitemb, quantity)
                        quantity = int(quantity)
                        bot.say(instigator + " traded " + str(quantitymath) + " "+ lootitem + "s for " +str(quantity) + " "+ lootitemb+ "s.")
                    
        ## Weaponslocker
        elif commandortarget == 'weaponslocker':
            target = get_trigger_arg(triggerargsarray, 2) or instigator
            validdirectionarray = ['total','inv','add','del','reset']
            if target in validdirectionarray:
                target = instigator
                adjustmentdirection = get_trigger_arg(triggerargsarray, 2).lower()
                weaponchange = get_trigger_arg(triggerargsarray, '3+')
            else:
                adjustmentdirection = get_trigger_arg(triggerargsarray, 3).lower()
                weaponchange = get_trigger_arg(triggerargsarray, '4+')
            weaponslist = get_database_value(bot, target, 'weaponslocker') or []
            statreset(bot, target)
            if not adjustmentdirection:
                bot.notice(instigator + ", Use .duel weaponslocker add/del to adjust Locker Inventory.", instigator)
            elif adjustmentdirection == 'total':
                gethowmany = get_database_array_total(bot, target, 'weaponslocker')
                bot.say(target + ' has ' + str(gethowmany) + " weapons in their locker. They Can be viewed in privmsg by running .duel weaponslocker inv")
            elif adjustmentdirection == 'inv':
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
                elif adjustmentdirection != 'add' and adjustmentdirection != 'del':
                    bot.say('Invalid Command.')
                elif adjustmentdirection == 'add' and weaponchange in weaponslist:
                    bot.notice(weaponchange + " is already in weapons locker.", instigator)
                elif adjustmentdirection == 'del' and weaponchange not in weaponslist:
                    bot.notice(weaponchange + " is already not in weapons locker.", instigator)
                elif adjustmentdirection == 'add' and len(weaponchange) > weaponmaxlength:
                    bot.notice("That weapon exceeds the character limit of "+str(weaponmaxlength)+".", instigator)
                else:
                    if adjustmentdirection == 'add':
                        weaponlockerstatus = 'now'
                    else:
                        weaponlockerstatus = 'no longer'
                    adjust_database_array(bot, target, weaponchange, 'weaponslocker', adjustmentdirection)
                    message = str(weaponchange + " is " + weaponlockerstatus + " in weapons locker.")
                    bot.notice(instigator + ", " + message, instigator)

        ## Magic
        elif commandortarget == 'magic':
            instigatorclass = get_database_value(bot, instigator, 'class')
            instigatormana = get_database_value(bot, instigator, 'mana')
            magicusage = get_trigger_arg(triggerargsarray, 2)
            if not magicusage or magicusage not in magicoptionsarray:
                magicoptions = get_trigger_arg(magicoptionsarray, 'list')
                bot.say('Magic uses include: '+ magicoptions)
            else:
                targnum = get_trigger_arg(triggerargsarray, 3).lower()
                if not targnum:
                    quantity = 1
                    target = instigator
                elif targnum.isdigit():
                    quantity = int(targnum)
                    target = instigator
                elif targnum.lower() in [x.lower() for x in dueloptedinarray]:
                    targnumb = get_trigger_arg(triggerargsarray, 4).lower()
                    target = targnum
                    if not targnumb:
                        quantity = 1
                    elif targnumb.isdigit():
                        quantity = int(targnumb)
                    elif targnumb == 'all':
                        quantity = int(gethowmanylootitem)
                    else:
                        bot.say("Invalid command.")
                        return
                elif target.lower() not in [x.lower() for x in dueloptedinarray]:
                    bot.notice(instigator + ", It looks like " + target + " has duels off.", instigator)
                elif target.lower() not in [u.lower() for u in bot.users]:
                    bot.notice(instigator + ", It looks like " + target + " is either not here, or not a valid person.", instigator)
                elif target == bot.nick:
                    bot.notice(instigator + ", I am immune to magic " + magicusage, instigator)
                elif not instigatormana:
                    bot.notice(instigator + " you don't have any mana.", instigator)
                else:
                    bot.say("Invalid command.")
                    return
                statreset(bot, target)
                healthcheck(bot, u)
                targetcurse = get_database_value(bot, target, 'curse') or 0
                targetclass = get_database_value(bot, target, 'class') or 'notclassy'
                if target.lower() != instigator.lower() and targetclass == 'fiend':
                    bot.notice(instigator + ", It looks like " + target + " is a fiend and can only self-use magic.", instigator)
                    manarequired = -abs(manarequired)
                    adjust_database_value(bot, instigator, 'mana', manarequired)
                elif magicusage == 'curse' and targetcurse:
                    bot.notice(instigator + " it looks like " + target + " is already cursed.", instigator)
                    return
                elif magicusage == 'curse':
                    manarequired = manarequiredmagiccurse
                elif magicusage == 'shield':
                    manarequired = manarequiredmagicshield
                else:
                    return
                if instigatorclass == 'mage':
                    manarequired = manarequired * magemanamagiccut
                actualmanarequired = int(manarequired) * int(quantity)
                manatier = tierratio_level(bot)
                actualmanarequired = actualmanarequired * manatier
                if int(actualmanarequired) > int(instigatormana):
                    manamath = int(int(actualmanarequired) - int(instigatormana))
                    bot.notice(instigator + " you need " + str(manamath) + " more mana to use magic " + magicusage + ".", instigator)
                else:
                    specialtext = ''
                    manarequired = -abs(actualmanarequired)
                    adjust_database_value(bot, instigator, 'mana', manarequired)
                    if magicusage == 'curse':
                        damagedealt = magiccursedamage
                        set_database_value(bot, target, 'curse', curseduration)
                        specialtext = str("which forces " + target + " to lose the next " + str(curseduration) + " duels AND deals " + str(abs(damagedealt))+ " damage.")
                        adjust_database_value(bot, target, 'health', int(damagedealt))
                    elif magicusage == 'shield':
                        damagedealt = magicshielddamage
                        actualshieldduration = int(quantity) * int(shieldduration)
                        adjust_database_value(bot, target, 'shield', actualshieldduration)
                        specialtext = str("which allows " + target + " to take no damage for the duration of " + str(actualshieldduration) + " damage AND restoring " +str(abs(damagedealt)) + " health.")
                        adjust_database_value(bot, target, 'health', int(damagedealt))
                    if instigator == target:
                        displaymsg = str(instigator + " uses magic " + magicusage + " " + specialtext + ".")
                    else:
                        displaymsg = str(instigator + " uses magic " + magicusage + " on " + target + " " + specialtext + ".")
                    bot.say(str(displaymsg))
                    if not inchannel.startswith("#") and target != instigator:
                        bot.notice(str(displaymsg), target)
                    instigatormana = get_database_value(bot, instigator, 'mana')
                    if instigatormana <= 0:
                        set_database_value(bot, instigator, 'mana', None)

        ## Admin Commands
        elif commandortarget == 'admin' and not trigger.admin:
            bot.notice(instigator + ", This is an admin only functionality.", instigator)
        elif commandortarget == 'admin':
            subcommand = get_trigger_arg(triggerargsarray, 2).lower()
            settingchange = get_trigger_arg(triggerargsarray, 3).lower()
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
                elif target.lower() not in [u.lower() for u in bot.users] and target != 'everyone':
                    bot.notice(instigator + ", It looks like " + str(target) + " is either not here, or not a valid person.", instigator)
                elif not subcommand:
                    bot.notice(instigator + ", Subcommand Missing. " + incorrectdisplay, instigator)
                elif subcommand not in statsadminchangearray:
                    bot.notice(instigator + ", Invalid subcommand. " + incorrectdisplay, instigator)
                elif not statset:
                    bot.notice(instigator + ", Stat Missing. " + incorrectdisplay, instigator)
                elif statset not in duelstatsadminarray and statset != 'all':
                    bot.notice(instigator + ", Invalid stat. " + incorrectdisplay, instigator)
                elif not trigger.admin:
                    bot.notice(instigator + "This is an admin only function.", instigator)
                else:
                    if subcommand == 'reset':
                        newvalue = None
                    if subcommand == 'set' and newvalue == None:
                        bot.notice(instigator + ", When using set, you must specify a value. " + incorrectdisplay, instigator)
                    elif target == 'everyone':
                        set_database_value(bot, duelrecorduser, 'chanstatsreset', now)
                        set_database_value(bot, duelrecorduser, 'levelingtier', None)
                        set_database_value(bot, duelrecorduser, 'specevent', None)
                        for u in bot.users:
                            statreset(bot, target)
                            if statset == 'all':
                                for x in duelstatsadminarray:
                                    set_database_value(bot, u, x, newvalue)
                            else:
                                set_database_value(bot, u, statset, newvalue)
                        bot.notice(instigator + ", Possibly done Adjusting stat(s).", instigator)
                    else:
                        statreset(bot, target)
                        try:
                            if newvalue.isdigit():
                                newvalue = int(newvalue)
                        except AttributeError:
                            newvalue = newvalue
                        if statset == 'all':
                            for x in duelstatsadminarray:
                                set_database_value(bot, target, x, newvalue)
                        else:
                            set_database_value(bot, target, statset, newvalue)
                        bot.notice(instigator + ", Possibly done Adjusting stat(s).", instigator)
            elif subcommand == 'resettier':
                set_database_value(bot, duelrecorduser, 'levelingtier', None)
            elif subcommand == 'bugbounty':
                target = get_trigger_arg(triggerargsarray, 3)
                statreset(bot, target)
                if not target:
                    bot.notice(instigator + ", Target Missing. ", instigator)
                elif target.lower() not in [u.lower() for u in bot.users]:
                    bot.notice(instigator + ", It looks like " + str(target) + " is either not here, or not a valid person.", instigator)
                elif not trigger.admin:
                    bot.notice(instigator + "This is an admin only function.", instigator)
                else:
                    bot.say(target + ' is awarded ' + str(bugbountycoinaward) + " coin for finding a bug in duels.")
                    adjust_database_value(bot, target, 'coin', bugbountycoinaward)
                    
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
             
        ## If not a command above, invalid
        else:
            bot.notice(instigator + ", It looks like " + str(commandortarget) + " is either not here, or not a valid person.", instigator)

    ## warning if user doesn't have duels enabled
    elif commandortarget.lower() not in [x.lower() for x in dueloptedinarray] and commandortarget != bot.nick:
        bot.notice(instigator + ", It looks like " + commandortarget + " has duels off.", instigator)
    
    ## Duels must be in a channel
    elif not inchannel.startswith("#"):
        bot.notice(instigator + ", Duels must be in a channel.", instigator)

    else:
        OSDTYPE = 'say'
        target = get_trigger_arg(triggerargsarray, 1)
        dowedisplay = 1
        executedueling = mustpassthesetoduel(bot, trigger, instigator, target, dowedisplay)
        if executedueling:
            targetarray.append(target)
            getreadytorumble(bot, trigger, instigator, targetarray, OSDTYPE, fullcommandused, now, triggerargsarray, typeofduel, inchannel)

    ## bot does not need stats or backpack items
    refreshbot(bot)

def getreadytorumble(bot, trigger, instigator, targetarray, OSDTYPE, fullcommandused, now, triggerargsarray, typeofduel, channel):
    
    assaultstatsarray = ['wins','losses','potionswon','potionslost','kills','deaths','damagetaken','damagedealt','levelups','xp']
    ## clean empty stats
    assaultdisplay = ''
    assault_xp, assault_wins, assault_losses, assault_potionswon, assault_potionslost, assault_deaths, assault_kills, assault_damagetaken, assault_damagedealt, assault_levelups = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

    targetarraytotal = len(targetarray)
    for target in targetarray:
        targetarraytotal = targetarraytotal - 1
        if typeofduel == 'assault':
            targetlastfoughtstart = get_database_value(bot, target, 'lastfought')
        
        ## verify stats aren't old
        statreset(bot, target)
        
        ## Special Event
        speceventtext = ''
        speceventtotal = get_database_value(bot, duelrecorduser, 'specevent') or 0
        if speceventtotal >= 49:
            set_database_value(bot, duelrecorduser, 'specevent', 1)
            speceventtext = str(instigator + " triggered the special event! Winnings are "+str(speceventreward)+" Coins!")
            adjust_database_value(bot, instigator, 'coin', speceventreward)
        else:
            adjust_database_value(bot, duelrecorduser, 'specevent', defaultadjust)
        
        ## Tier update
        currenttierstart = get_database_value(bot, duelrecorduser, 'levelingtier') or 0

        ## Update Time Of Combat
        set_database_value(bot, instigator, 'timeout', now)
        set_database_value(bot, target, 'timeout', now)
        set_database_value(bot, duelrecorduser, 'timeout', now)

        ## Naming and Initial pepper level
        instigatorname, instigatorpepperstart = whatsyourname(bot, trigger, instigator, channel)
        if instigator == target:
            targetname = "themself"
            targetpepperstart = ''
        else:
            targetname, targetpepperstart = whatsyourname(bot, trigger, target, channel)

        ## Magic Attributes Start
        instigatorshieldstart, targetshieldstart, instigatorcursestart, targetcursestart = get_current_magic_attributes(bot, instigator, target)

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

        ## classes
        yourclasswinner = get_database_value(bot, winner, 'class') or 'notclassy'
        yourclassloser = get_database_value(bot, loser, 'class') or 'notclassy'

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

        ## Damage Done (random)
        damage, winnermsg = damagedone(bot, winner, loser, weapon, 1)
        
        ## Update Wins and Losses
        if instigator != target:
            adjust_database_value(bot, winner, 'wins', defaultadjust)
            adjust_database_value(bot, loser, 'losses', defaultadjust)
            set_current_streaks(bot, winner, 'win')
            set_current_streaks(bot, loser, 'loss')

        ## Update last fought
        if instigator != target:
            set_database_value(bot, instigator, 'lastfought', target)
            set_database_value(bot, target, 'lastfought', instigator)

        ## Same person can't instigate twice in a row
        set_database_value(bot, duelrecorduser, 'lastinstigator', instigator)

        ## Update Health Of Loser, respawn, allow winner to loot
        currenthealth = get_database_value(bot, loser, 'health')
        if instigator == target:
            loser = targetname
        if currenthealth <= 0:
            whokilledwhom(bot, winner, loser)
            winnermsg = str(winnermsg +  loser + ' dies forcing a respawn!!')
            if winner == instigator:
                assault_kills = assault_kills + 1
            else:
                assault_deaths = assault_deaths + 1

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
            loot_text = eval(loot+"dispmsg")
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

        ## Tier update Part 2
        tierchangemsg = ''
        currenttierend = get_database_value(bot, duelrecorduser, 'levelingtier') or 1
        if int(currenttierend) > int(currenttierstart):
            tierchangemsg = str("New Tier Unlocked!")
            if currenttierend != 1:
                newtierlistarray = []
                for x in tiercommandarray:
                    newtiereval = eval("tierunlock"+x)
                    if newtiereval == currenttierend:
                        newtierlistarray.append(x)
                if newtierlistarray != []:
                    newtierlist = get_trigger_arg(newtierlistarray, "list")
                    tierchangemsg = str(tierchangemsg + " Function(s) now available: " + newtierlist)
                
        ## Update XP points
        if yourclasswinner == 'ranger':
            XPearnedwinner = XPearnedwinnerranger
        else:
            XPearnedwinner = XPearnedwinnerstock
        if yourclassloser == 'ranger':
            XPearnedloser = XPearnedloserranger
        else:
            XPearnedloser = XPearnedloserstock
        if instigator != target:
            winnertier = get_database_value(bot, winner, 'levelingtier')
            losertier = get_database_value(bot, loser, 'levelingtier')
            xptier = tierratio_level(bot)
            if winnertier < currenttierend:
                XPearnedwinner = XPearnedwinner * xptier
            if losertier < currenttierend:
                XPearnedloser = XPearnedloser * xptier
            adjust_database_value(bot, winner, 'xp', XPearnedwinner)
            adjust_database_value(bot, loser, 'xp', XPearnedloser)
        
        ## On Screen Text
        combattextarrayloop = ['announcecombatmsg','lootwinnermsg','winnermsg','lootwinnermsgb','pepperstatuschangemsg','magicattributestext','speceventtext','tierchangemsg']
        lastarray = 2
        combattextarraya = []
        combattextarrayb = []
        for x in combattextarrayloop:
            checktext = eval(x)
            if checktext and checktext != '':
                if lastarray == 2:
                    combattextarraya.append(checktext)
                    lastarray = 1
                else:
                    if x == 'winnermsg':
                        combattextarrayb.append("dummytext")
                        combattextarraya.append(checktext)
                        lastarray = 1
                    else:
                        combattextarrayb.append(checktext)
                        lastarray = 2
        if len(combattextarraya) > len(combattextarrayb):
            combattextarrayb.append("dummytext")
        for arrayone, arraytwo in zip(combattextarraya, combattextarrayb):
            if arraytwo == "dummytext":
                arraytwo = ''
            if OSDTYPE == 'say':
                bot.say(arrayone + "   " + arraytwo)
            elif OSDTYPE == 'notice':
                bot.notice(arrayone + "   " + arraytwo, winner)
                bot.notice(arrayone + "   " + arraytwo, loser)
        
        ## update assault stats
        if winner == instigator:
            assault_wins = assault_wins + 1
            assault_damagedealt = assault_damagedealt + int(damage)
            assault_xp = assault_xp + XPearnedwinner
            if yourclasswinner == 'vampire':
                assault_damagetaken = assault_damagetaken - int(damage)
        if loser == instigator:
            assault_losses = assault_losses + 1
            assault_damagetaken = assault_damagetaken + int(damage)
            assault_xp = assault_xp + XPearnedloser

        ## Pause Between duels
        if targetarraytotal > 0 and typeofduel == 'assault':
            bot.notice("  ", instigator)
            time.sleep(5)
        
        ## Random Bonus
        if typeofduel == 'random' and winner == instigator:
            adjust_database_value(bot, winner, 'coin', randomcoinaward)
            
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
    duelusersarray = get_database_value(bot, bot.nick, 'duelusers')
    for u in bot.users:
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

            ## award coin to scavengers
            if uclass == 'scavenger':
                adjust_database_value(bot, u, 'coin', scavengercoinaward)

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
        loot_text = str(mysterypotiondispmsg + " Use .duel loot use mysterypotion to consume.")
        adjust_database_value(bot, lootwinner, 'mysterypotion', defaultadjust)
        lootwinnermsg = str(lootwinner + ' is awarded a mysterypotion ' + str(loot_text))
        bot.notice(lootwinnermsg, lootwinner)

    ## bot does not need stats or backpack items
    refreshbot(bot)

## Functions ######################################################################################################################

######################
## Criteria to duel ##
######################

def mustpassthesetoduel(bot, trigger, instigator, target, dowedisplay):
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

    if instigator == duelrecorduserlastinstigator and instigatortime <= INSTIGATORTIMEOUT and not bot.nick.endswith(devbot):
        displaymsg = str("You may not instigate fights twice in a row within a half hour. You must wait for somebody else to instigate, or "+str(hours_minutes_seconds((INSTIGATORTIMEOUT - instigatortime)))+" .")
    elif target == instigatorlastfought and not bot.nick.endswith(devbot) and howmanyduelsers > 2:
        displaymsg = str(instigator + ', You may not fight the same person twice in a row.')
    elif instigator.lower() not in [x.lower() for x in dueloptedinarray]:
        displaymsg = str(instigator + ", It looks like you have disabled duels. Run .duel on to re-enable.")
    elif target.lower() not in [x.lower() for x in dueloptedinarray]:
        displaymsg = str(instigator + ', It looks like ' + target + ' has disabled duels.')
    elif instigatortime <= USERTIMEOUT and not bot.nick.endswith(devbot):
        displaymsg = str("You can't duel for "+str(hours_minutes_seconds((USERTIMEOUT - instigatortime)))+".")
    elif targettime <= USERTIMEOUT and not bot.nick.endswith(devbot):
        displaymsg = str(target + " can't duel for "+str(hours_minutes_seconds((USERTIMEOUT - targettime)))+".")
    elif duelrecordusertime <= CHANTIMEOUT and not bot.nick.endswith(devbot):
        displaymsg = str("Channel can't duel for "+str(hours_minutes_seconds((CHANTIMEOUT - duelrecordusertime)))+".")
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
    healthcheck(bot, loser)
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
    if not health or health < 0:
        if nick != bot.nick:
            currenthealthtier = tierratio_level(bot)
            currenthealthtier = currenthealthtier * stockhealth
            set_database_value(bot, nick, 'health', currenthealthtier)
    ## no mana at respawn
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
        timediff = str(hours_minutes_seconds((USERTIMEOUT - time_since)))
    else:
        timediff = 0
    return timediff

def hours_minutes_seconds(countdownseconds):
    time = float(countdownseconds)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minute = time // 60
    time %= 60
    second = time
    displaymsg = ''
    timearray = ['hour','minute','second']
    for x in timearray:
        currenttimevar = eval(x)
        if currenttimevar >= 1:
            timetype = x
            if currenttimevar > 1:
                timetype = str(x+"s")
            displaymsg = str(displaymsg + str(int(currenttimevar)) + " " + timetype + " ")
    return displaymsg

###########
## Names ##
###########

def whatsyourname(bot, trigger, nick, channel):
    nickname = str(nick)
    
    ## Pepper Level
    pepperstart = get_pepper(bot, nick)
    
    ## custom title
    nicktitle = get_database_value(bot, nick, 'title')
    
    ## bot.owner
    try:
        if nicktitle:
            nickname = str(nicktitle+" " + nickname)
        elif nick.lower() in bot.config.core.owner.lower():
            nickname = str("The Legendary " + nickname)
    ## botdevteam
        elif nick in botdevteam:
            nickname = str("The Extraordinary " + nickname)
    ## OP
        elif bot.privileges[channel.lower()][nick.lower()] == OP:
            nickname = str("The Magnificent " + nickname)
    ## VOICE
        elif bot.privileges[channel.lower()][nick.lower()] == VOICE:
            nickname = str("The Incredible " + nickname)
    ## bot.admin
        elif nick in bot.config.core.admins:
            nickname = str("The Spectacular " + nickname)
    ## else
        else:
            nickname = str(nickname)
    except KeyError:
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
    if not pepperstart or pepperstart == '':
        nickname = str(nickname + " (n00b)")
    else:
        nickname = str(nickname + " (" + pepperstart + ")")

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
        if len(x) > weaponmaxlength:
            adjust_database_array(bot, nick, x, 'weaponslocker', 'del')
        if x not in lastusedweaponarry and x != lastusedweapon and len(x) <= weaponmaxlength:
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

################
## Stat Reset ##
################

def statreset(bot, nick):
    now = time.time()
    getlastchanstatreset = get_database_value(bot, duelrecorduser, 'chanstatsreset')
    if not getlastchanstatreset:
        set_database_value(bot, duelrecorduser, 'chanstatsreset', now)
    getnicklastreset = get_database_value(bot, nick, 'chanstatsreset')
    if getnicklastreset < getlastchanstatreset:
        for x in duelstatsadminarray:
            set_database_value(bot, nick, x, None)
        set_database_value(bot, nick, 'chanstatsreset', now)

################
## Tier ratio ##
################

def tierratio_level(bot):
    currenttier = get_database_value(bot, duelrecorduser, 'levelingtier')
    if not currenttier:
        tierratio = stocktierratio
    else:
        wordconvert = num2words(int(currenttier))
        tierratio = eval("tierratio"+ wordconvert)
    return tierratio

#################
## Damage Done ##
#################

def damagedone(bot, winner, loser, weapon, diaglevel):
    damagescale = tierratio_level(bot)
    winnerclass = get_database_value(bot, winner, 'class') or 'notclassy'
    loserclass = get_database_value(bot, loser, 'class') or 'notclassy'
    shieldloser = get_database_value(bot, loser, 'shield') or 0
    shieldwinner = get_database_value(bot, winner, 'shield') or 0
    damagetext = ''
    
    ## names
    if winner == 'duelsroulettegame':
        winnername = loser
        losername = "themself"
        striketype = "shoots"
    elif winnerclass == 'knight' and diaglevel == 2:
        winnername = winner
        losername = loser
        striketype = "retaliates against"
    else:
        winnername = winner
        losername = loser
        striketype = "hits"
    
    ## Rogue can't be hurt by themselves or bot
    roguearraynodamage = [bot.nick,loser]
    if loserclass == 'rogue' and winner in roguearraynodamage:
        damage = 0
    
    elif winner == 'duelsroulettegame':
        damage = randint(50, 120)
    
    ## Bot deals a set amount
    elif winner == bot.nick:
        damage = botdamage

    ## Barbarians get extra damage (minimum)
    elif winnerclass == 'barbarian':
        damage = randint(barbarianminimumdamge, 120)
    
    ## vampires have a minimum damage
    elif winnerclass == 'vampire':
        damage = randint(0, vampiremaximumdamge)
    
    ## All Other Players
    else:
        damage = randint(0, 120)
       
    ## Damage Tiers
    if damage > 0:
        damage = damagescale * damage
        damage = int(damage)

    if damage == 0:
        damagetext = str(winnername + " "+striketype+" " + losername + weapon + ' but deals no damage. ')
    elif winnerclass == 'vampire':
        damagetext = str(winnername + " drains " + str(damage)+ " health from " + losername + weapon + ". ")
    else:
        damagetext = str(winnername + " "+striketype+" " + losername + weapon + ', striking a blow of ' + str(damage) + ' damage. ')
    
    ## Vampires gain health from wins
    if winnerclass == 'vampire':
        adjust_database_value(bot, winner, 'health', damage)
        
    ## Berserker Rage
    if winnerclass == 'barbarian':
        rageodds = randint(1, 12)
        if rageodds == 1:
            extradamage = randint(1, 25)
            damagetext = str(damagetext +" "+ winner + " goes into Berserker Rage for an extra " + str(extradamage) + " damage. ")
            damage = damage + extradamage
    
    ## Paladin deflect
    if loserclass == 'paladin' and damage > 0 and winner != 'duelsroulettegame':
        deflectodds = randint(1, 12)
        if deflectodds == 1:
            damageb = damage
            damage = 0
            damagetext = str(damagetext + " "+ losername + " deflects the damage back on " + winnername + ". ")
            damagemathb = int(shieldwinner) - damageb
            if int(damagemathb) > 0:
                adjust_database_value(bot, winner, 'shield', -abs(damageb))
                damageb = 0
                absorbedb = 'all'
            else:
                absorbedb = damagemathb + damageb
                damage = abs(damagemathb)
                set_database_value(bot, loser, 'shield', None)
            damagetext = str(damagetext + " "+ winnername + " absorbs " + str(absorbedb) + " of the damage. ")
    
    ## Shield resistance
    if shieldloser and damage > 0:
        damagemath = int(shieldloser) - damage
        if int(damagemath) > 0:
            adjust_database_value(bot, loser, 'shield', -abs(damage))
            damage = 0
            absorbed = 'all'
        else:
            absorbed = damagemath + damage
            damage = abs(damagemath)
            set_database_value(bot, loser, 'shield', None)
        damagetext = str(damagetext + " "+ losername + " absorbs " + str(absorbed) + " of the damage. ")

    ## Knight
    if loserclass == 'knight' and diaglevel != 2 and winner != 'duelsroulettegame':
        retaliateodds = randint(1, 12)
        if retaliateodds == 1:
            weaponb = weaponofchoice(bot, loser)
            weaponb = weaponformatter(bot, weaponb)
            weaponb = str(" "+ weaponb)
            damageb, damagetextb = damagedone(bot, loser, winner, weaponb, 2)
            damagetext = str(damagetext + " "+damagetextb)
            
    ## dish it out
    if damage > 0:
        adjust_database_value(bot, loser, 'health', -abs(damage))
    
    return damage, damagetext

##################
## Pepper level ##
##################

def get_pepper(bot, nick):
    tiernumber = 0
    nicktier = get_database_value(bot, nick, 'levelingtier')
    nickpepper = get_database_value(bot, nick, 'levelingpepper')
    currenttier = get_database_value(bot, duelrecorduser, 'levelingtier')
    xp = get_database_value(bot, nick, 'xp')
    if nick == bot.nick:
        pepper = 'Dragon Breath Chilli'
    elif not xp:
        pepper = ''
    elif xp > 0 and xp < 100:
        pepper = 'Pimiento'
        tiernumber = 1
    elif xp >= 100 and xp < 250:
        pepper = 'Sonora'
        tiernumber = 2
    elif xp >= 250 and xp < 500:
        pepper = 'Anaheim'
        tiernumber = 3
    elif xp >= 500 and xp < 1000:
        pepper = 'Poblano'
        tiernumber = 4
    elif xp >= 1000 and xp < 2500:
        pepper = 'Jalapeno'
        tiernumber = 5
    elif xp >= 2500 and xp < 5000:
        pepper = 'Serrano'
        tiernumber = 6
    elif xp >= 5000 and xp < 7500:
        pepper = 'Chipotle'
        tiernumber = 7
    elif xp >= 7500 and xp < 10000:
        pepper = 'Tabasco'
        tiernumber = 8
    elif xp >= 10000 and xp < 15000:
        pepper = 'Cayenne'
        tiernumber = 9
    elif xp >= 15000 and xp < 25000:
        pepper = 'Thai Pepper'
        tiernumber = 10
    elif xp >= 25000 and xp < 45000:
        pepper = 'Datil'
        tiernumber = 11
    elif xp >= 45000 and xp < 70000:
        pepper = 'Habanero'
        tiernumber = 12
    elif xp >= 70000 and xp < 100000:
        pepper = 'Ghost Chili'
        tiernumber = 13
    elif xp >= 100000 and xp < 250000:
        pepper = 'Mace'
        tiernumber = 14
    elif xp >= 250000:
        pepper = 'Pure Capsaicin'
        tiernumber = 15
    
    ## advance respawn tier
    if tiernumber > currenttier:
        set_database_value(bot, duelrecorduser, 'levelingtier', tiernumber)
    if tiernumber != nicktier:
        set_database_value(bot, nick, 'levelingtier', tiernumber)
    #if pepper != nickpepper:
    #    set_database_value(bot, nick, 'levelingpepper', pepper)
    
    return pepper

def get_tierpepper(bot, tiernumber):
    if not tiernumber:
        pepper = ''
    elif tiernumber == 1:
        pepper = 'Pimiento'
    elif tiernumber == 2:
        pepper = 'Sonora'
    elif tiernumber == 3:
        pepper = 'Anaheim'
    elif tiernumber == 4:
        pepper = 'Poblano'
    elif tiernumber == 5:
        pepper = 'Jalapeno'
    elif tiernumber == 6:
        pepper = 'Serrano'
    elif tiernumber == 7:
        pepper = 'Chipotle'
    elif tiernumber == 8:
        pepper = 'Tabasco'
    elif tiernumber == 9:
        pepper = 'Cayenne'
    elif tiernumber == 10:
        pepper = 'Thai Pepper'
    elif tiernumber == 11:
        pepper = 'Datil'
    elif tiernumber == 12:
        tiernumber = 12
    elif tiernumber == 13:
        pepper = 'Ghost Chili'
    elif tiernumber == 14:
        pepper = 'Mace'
    elif tiernumber == 15:
        pepper = 'Pure Capsaicin'
    else:
        pepper = ''
    return pepper


###################
## Select Winner ##
###################

def selectwinner(bot, nickarray):
    statcheckarray = ['health','xp','kills','respawns','currentwinstreak']

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
        if x == 'respawns' or x == 'currentwinstreak':
            statscore = 99999999
        statleader = ''
        for u in nickarray:
            value = get_database_value(bot, u, x) or 0
            if x == 'respawns' or x == 'currentwinstreak':
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
        cursed = get_database_value(bot, user, 'curse') or 0
        if cursed:
            set_database_value(bot, user, 'winnerselection', None)
            adjust_database_value(bot, user, 'curse', -1)

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
        rolla = 8
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
    if not losses:
        if not wins:
            winlossratio = 0
        else:
            winlossratio = wins
    else:
        winlossratio = float(wins)/losses
    return winlossratio

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
