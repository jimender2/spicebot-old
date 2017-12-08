import sopel.module
import sys
import os
import random
import Spicebucks
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
    if len(triggerargsarray) < 5:
       bot.say("You must enter 5 lottery numbers from 1 to 20 to play.")
    elif len(triggerargsarray) > 5
       bot.say("You must enter 5 lottery numbers from 1 to 20 to play.")
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
        pickstemp = picks
        picks = []
        for pick in pickstemp:
            if pick not in picks:
                picks.append(pick)
        if len(picks) < 5:
            bot.say("You must have a duplicate in your picks.")
            success = 0
        if success == 1:
            valid = 1
            for pick in picks:
                if pick > 20 or pick < 1:
                    valid = 0
            if valid == 0:
                bot.say("One of the numbers you entered does is not within the 1 to 20 range.")
            else:
                if Spicebucks.spicebucks(bot, trigger.nick, 'minus', 1) == 'true':
                    winningnumbers = random.sample(range(1, 20), 5) 
                    bot.say('The winning numbers are ' + str(winningnumbers))
                    correct = 0
                    for pick in picks:
                        if pick in winningnumbers:
                            correct = correct + 1
                    payout = 0
                    if correct == 1:
                        payout = 1
                    elif correct == 2:
                        payout = 2
                    elif correct == 3:
                        payout = 5
                    elif correct == 4:
                        payout = 20
                    elif correct == 5:
                        payout = 50
                    Spicebucks.spicebucks(bot, trigger.nick, 'plus', payout)
                    bot.say("You guessed " + str(correct) + " numbers correctly, and were paid " + str(payout) + " spicebucks.")
