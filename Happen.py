import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('happen')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    happen = get_trigger_arg(triggerargsarray, 1)
    if not happen:
        bot.say("Stop trying to make stuff happen. It's not going to happen")
    else:
        bot.say("Stop trying to make " + str(happen) + " happen. It's not going to happen")
