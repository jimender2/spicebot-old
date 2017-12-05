import sopel.module
import sys
import os
import random
import Points
import string
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('lottery')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    if len(triggerargsarray) < 6:
       bot.say("You must enter 5 lottery numbers betwen from 1 to 50 to play.")
    else:
        success = 0
        picks = []
        try:
            for pick in triggerargsarray:
                picks.append(int(pick))
            success = 1
        except:
            bot.say("One of the numbers you entered does not appear to be a number.")
            success = 0
        
        if success = 1:
            valid = 1
            for pick in picks:
                if pick > 50 or pick < 1:
                    valid = 0
            if valid == 0:
                bot.say("One of the numbers you entered does is not within the 1 to 50 range.")
            else:
                winningnumbers = random.sample(range(1, 50, 5)    
                bot.say('The winning numbers are ' + str(winningnumbers))
                
