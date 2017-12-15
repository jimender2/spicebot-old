import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('usage')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    ## Initial ARGS of importance
    usagefor = ''
    triggerargsarray = create_args_array(trigger.group(2))
    commandused = get_trigger_arg(triggerargsarray, 0)
    moduletocheck = get_trigger_arg(triggerargsarray, 1)
    checktarget = get_trigger_arg(triggerargsarray, 2)
    if checktarget:
        usagefor = checktarget
    elif not checktarget:
        usagefor = trigger.nick
    
    count = get_database_value(bot, usagefor, moduletocheck+"usage")
    
    ##says the variables
    bot.action("checks usage of " + moduletocheck + " for " + usagefor + " " + count)
