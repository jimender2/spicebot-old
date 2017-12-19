import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('nelson')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    instigator = trigger.nick
    for c in bot.channels:
        channel = c
    target = get_trigger_arg(triggerargsarray, 1)
    if not target:
        bot.say("Who are we laughing at?")
    elif target == instigator:
        bot.say('Is your self esteem really that low?')
    elif target.lower() not in bot.privileges[channel.lower()]:
        bot.say("I'm not sure who that is.")
    elif target == bot.nick:
        bot.say("I like to laugh, but not at my own expense.")
    else:
        message = str(bot.nick + " points at " + target + " and laughs.")
        bot.say(message)
