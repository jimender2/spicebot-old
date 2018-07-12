#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel
from sopel import module, tools
import random
from random import randint
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *
import Spicebucks

#hungergamesfee=5

@sopel.module.commands('hungergames')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)

def execute_main(bot, trigger, triggerargsarray):
    randomtargetarray = []
    botusersarray = get_botdatabase_value(bot, bot.nick, 'botusers') or []
    for u in bot.users:
        if u in botusersarray and u != bot.nick:
            randomtargetarray.append(u)
    if randomtargetarray == []:
        bot.say("There is currently no one available to play the hunger games.")
    else:
        random.shuffle(randomtargetarray)
        totaltributes = len(randomtargetarray)
        if totaltributes == 1:
            bot.say("There is only one tribute.  Try again later.")
        else:
            bot.say("Let the Hunger Games begin!  May the odds be ever in your favor.")
            if totaltributes == 2:
                bot.say("The victor is " + str(randomtargetarray[0]))
            elif totaltributes == 3:
                bot.say("The first to die was " + str(randomtargetarray[1]) + " The victor is " + str(randomtargetarray[0]))
            else:
                #safetribute = str(randomtargetarray[2])
                #volunteer = str(randomtargetarray[3])
                #randomtargetarray.pop(2)
                #random.shuffle(randomtargetarray)
                #bot.say(volunteer + " volunteered as tribute for " + safetribute + ". The first to die was " + str(randomtargetarray[1]) + ". The victor is " + str(randomtargetarray[0]))
                tributes = []
                weapons = ['dagger','sword','knife','bow and arrow', 'crossbow']
                for tribute in randomtargetarray:
                    random.shuffle(weapons)
                    tributerow = [tribute, 100, weapons[0]]
                    tributes.append(tributerow)
                totaltributes = len(tributes)
                while totaltributes > 1:
                    random.shuffle(tributes)
                    damageone = randint(50, 80)
                    damagetwo = randint(50, 80)
                    if damagetwo == damageone:
                        while damageone == damagetwo:
                            damageone = randint(50, 80)
                            damagetwo = randint(50, 80)
                    bot.notice(tributes[0][0] + " hits " + tributes[1][0] + " with a " + tributes[0][2] + "(-" + str(damageone) + "). " + tributes[1][0] + " hits " + tributes[0][0] + " with a " + tributes[1][2] + "(-" + str(damagetwo) + "). ", trigger.nick)
                    tributes[0][1] = tributes[0][1] - damageone
                    tributes[1][1] = tributes[1][1] - damageone
                    if tributes[0][1] <= 0:
                        bot.notice(tributes[1][0] + " killed " + tributes[0][0], trigger.nick)
                    if tributes[1][1] <= 0:
                        if len(tributes) > 1:
                            bot.notice(tributes[0][0] + " killed " + tributes[1][0], trigger.nick)
                    if tributes[1][1] <= 0: #remove second tribute first is killed to not mess up order if first is killed
                        tributes.pop(1)
                    if tributes[0][1] <= 0:
                        if len(tributes) > 1:
                            tributes.pop(0)
                    totaltributes = len(tributes)
                #payout =randint(hungergamesfee,35)
                bot.say("The victor is " + tributes[0][0])
                    #Spicebucks.spicebucks(bot,tributes[0][0],'plus',payout)
        #else:
            #bot.notice("It costs " + str(hungergamesfee) + " to play HungerGames.",trigger.nick)
