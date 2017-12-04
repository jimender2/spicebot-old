import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.require_admin
@sopel.module.commands('argtest')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    newvalue = get_trigger_arg(triggerargsarray, '5+')
    arg = get_trigger_arg(triggerargsarray, 4)
    totalarray = len(triggerargsarray)
    for i in range(1,totalarray):
        arg = get_trigger_arg(triggerargsarray, i)
        bot.say("arg" + str(i) + " = " + str(arg))
    bot.say("simulating arg5+ " + str(newvalue))
