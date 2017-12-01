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
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)

def execute_main(bot, trigger):
    enteredValues = string.split(trigger.args[1], " ")
    if len.enteredValues <= 6:
        bot.notify('You must enter 5 lottery numbers to play.')
    else:
        Points.pointstask(bot, channel, 'Entering the lottery', trigger.nick, ' takes ', ' from', 'down', 'points', trigger.sender)
        winningnumbers = random.sample(range(1, 100), 5)    
        bot.say('The winning numbers are ' + winningnumbers)    
        
