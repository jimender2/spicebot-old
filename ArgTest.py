import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('argtest')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    totalarray = len(triggerargsarray)
    bot.say(str(triggerargsarray))
    bot.say(str(totalarray))
    for i in range(1,20):
        arg = get_trigger_arg(triggerargsarray, i)
        bot.say(str(arg))


