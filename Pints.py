import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('pints','pint')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    if not trigger.group(2):
        winner = "Everybody"
    else:
        winner = trigger.group(2).strip()
        if trigger.group(2) == 'all':
            winner = "Everybody"
        elif trigger.group(2) == trigger.nick:
            winner = "him/her-self"
    bot.say(trigger.nick + ' buys a pint for ' + winner)
