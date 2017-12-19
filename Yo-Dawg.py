import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('yodawg')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    target = get_trigger_arg(triggerargsarray, 1)
     for c in bot.channels:
        channel = c
    if target:
        statement = str("Yo Dawg! I heard you liked " + target + ", So I put a " + target + " in/on your " + target + "!!!")
        bot.say(statement)
    else:
        bot.say("I'm not sure who that is.")
