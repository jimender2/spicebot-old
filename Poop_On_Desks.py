import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('poop','poops')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    target = get_trigger_arg(triggerargsarray, 1)
    if not target:
        bot.say(trigger.nick + ' poops in the designated corner!')
    elif target == 'group':
        bot.say(trigger.nick + ', get your poop in a group.')
    elif target == 'all' or target == 'everyone' or target == 'everyones':
        bot.say(trigger.nick + " poops on everyone's desk, one at a time!")
    elif target != bot.nick:
        if myline.endswith('desk'):
            bot.say(trigger.nick + ' poops on ' + target + ", maintaining eye contact the entire time!")
        else:
            bot.say(trigger.nick + ' poops on ' + target + "'s desk, maintaining eye contact the entire time!")
