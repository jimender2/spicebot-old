import sopel
from sopel import module, tools
import random
from random import randint
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('hungergames')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    randomtargetarray = []
    for c in bot.channels:
        channel = c
    for u in bot.channels[channel].users:
        target = u
        disenable = get_botdatabase_value(bot, target, 'disenable')
        if disenable:
            randomtargetarray.append(target)
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
                weapons = ['dagger','sword','knife','bow and arrow']
                for tribute in randomtargetarray:
                    random.shuffle(weapons)
                    tributerow = [tribute, 100, weapons[0]]
                    tributes.append(tributerow)
                totaltributes = len(tributes)
                deathorder = ''
                while totaltributes > 1:
                    random.shuffle(tributes)
                    damageone = randint(10, 30)
                    damagetwo = randint(10, 30)
                    bot.say(tributes[0][0] + " hits " + tributes[1][0] + " with a " + tributes[0][2] + "(-" + str(damageone) + "). " + tributes[1][0] + " hits " + tributes[0][0] + " with a " + tributes[1][2] + "(-" + str(damagetwo) + "). ")
                    tributes[0][1] = tributes[0][1] - damageone
                    tributes[1][1] = tributes[1][1] - damageone
                    if tributes[0][1] <= 0:
                        bot.say(tributes[1][0] + " killed " + tributes[0][0])
                    if tributes[1][1] <= 0:
                        if len(tributes) > 1:
                            bot.say(tributes[0][0] + " killed " + tributes[1][0])
                    if tributes[1][1] <= 0: #remove second tribute first is killed to not mess up order if first is killed
                        deathorder = str(totaltributes) + ": " + tributes[1][0] + " " + deathorder
                        tributes.pop(1)
                    if tributes[0][1] <= 0:
                        if len(tributes) > 1:
                            deathorder = str(totaltributes) + ": " + tributes[0][0] + " " + deathorder
                            tributes.pop(0)
                    totaltributes = len(tributes)
                bot.say("The victor is " + tributes[0][0])
                deathorder = "1: " + tributes[0][0] + " " + deathorder
                bot.say(deathorder)
                        
                        
