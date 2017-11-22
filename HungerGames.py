import sopel
from sopel import module, tools
import random
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('hungergames')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    randomtargetarray = []
    for c in bot.channels:
        channel = c
    for u in bot.channels[channel].users:
        target = u
        #targetdisenable = get_database_value(bot, target, 'disenable')
        #if targetdisenabled:
        randomtargetarray.append(target) ##need to filter out those with spicebot disabled
        if randomtargetarray == []:
            bot.say("There is currently no one available to play the hunger games.")
        else:      
            random.shuffle(randomtargetarray)
            totaltributes = len(randomtargetarray)
            bot.say("Currently there are " + totaltributes + " tributes (to be removed).")
            if totaltributes == 1:
                bot.say("There is only one tribute.  Try again later.")
            else:
                bot.say("Let the Hunger Games begin!  May the odds be ever in your favor.")
                if totaltributes == 2:
                    bot.say("The victor is " + str(randomtargetarray[0]))
                elif totaltributes == 3:
                    bot.say("The first to die was " + str(randomtargetarray[1]) + " The victor is " + str(randomtargetarray[0]))
                else:
                    safetribute = str(randomtargetarray[2])
                    volunteer = str(randomtargetarray[3])
                    randomtargetarray.pop(2)
                    random.shuffle(randomtargetarray)
                    bot.say(volunteer + " volunteered for " + safetribute + ". The first to die was " + str(randomtargetarray[1]) + ". The victor is " + str(randomtargetarray[0]))
