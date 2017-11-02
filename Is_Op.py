import sopel.module
from sopel.module import OP
from sopel.tools.target import User, Channel
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('isop')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    if not trigger.group(2):
        nick = trigger.nick.lower()
    else:
        nick = trigger.group(2).lower()
    try:    
        if bot.privileges[trigger.sender][nick] == OP:
            bot.say(nick + ' is an op.')
        else: 
            bot.say(nick + ' is not an op.')
    except KeyError:
        bot.say(nick + ' is not here right now!')
