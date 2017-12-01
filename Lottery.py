import sopel.module
import sys
import os
import random
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('lottery')
def mainfunction(bot, trigger):
    if not trigger.group(7):
        bot.notify('You must enter 5 numbers to enter the lottery.')
    else:
        if not float(trigger.group(3)).is_integer() and not float(trigger.group(4)).is_integer() and not float(trigger.group(5)).is_integer() and not float(trigger.group(6)).is_integer() and not float(trigger.group(7)).is_integer():
            bot.notify('One of the values you entered does not appear to be a number.')
        else:
            if not enablestatus:
                execute_main(bot, trigger)

def execute_main(bot, trigger):
    import Points
    Points.pointstask(bot, channel, 'Entering the lottery', trigger.nick, ' takes ', ' from', 'down', 'points', trigger.sender)
    #Get the numbers
    winningnumbers = random.sample(range(1, 100), 5)
    bot.say('The winning numbers are ' + winningnumbers)
    
