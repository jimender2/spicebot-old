import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('goldstar')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    target = get_trigger_arg(triggerargsarray, 1)
    for c in bot.channels:
        channel = c
    if not target:
        bot.say("Who deserves a gold star?")
    elif target.lower() not in bot.privileges[channel.lower()]:
        bot.say("I'm not sure who that is.")
    elif target == bot.nick:
        bot.action("blushes",channel)
    else:
        bot.say(trigger.nick + " gives " + target + " a gold star for participation.")
