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
        if checktarget == 'channel':
            usagefor = trigger.sender
        else:
            usagefor = checktarget
    elif not checktarget:
        usagefor = str(trigger.nick)
    count = get_botdatabase_value(bot, usagefor, moduletocheck+"usage")
    
    if count == 0:
        message = str('It appears that ' + usagefor + ' has not run ' + moduletocheck + ' at all.')
    elif count == 1:
        message = str(usagefor + ' has run ' + moduletocheck + ' a total of ' + str(count) + ' time.')
    else:
        message = str(usagefor + ' has run ' + moduletocheck + ' a total of ' + str(count) + ' times.')
    ##says the variables
    #bot.action("checks usage of " + moduletocheck + " for " + usagefor + " " + str(count))
    bot.say(message)
