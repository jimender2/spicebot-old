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
    querytype = 'specific'
    instigator = trigger.nick
    triggerargsarray = create_args_array(trigger.group(2))
    commandused = get_trigger_arg(triggerargsarray, 0)
    moduletocheck = get_trigger_arg(triggerargsarray, 1) or instigator
    checktarget = get_trigger_arg(triggerargsarray, 2)
    for c in bot.channels:
        channel = c

    if moduletocheck == 'me':
        moduletocheck = trigger.nick
    if moduletocheck == 'channel'
        querytype = 'invalidmodule'
    if moduletocheck == 'help':
        querytype = 'help'
    if moduletocheck.lower() in bot.privileges[channel.lower()]:
        querytype = 'user'
        usagefor = str(moduletocheck)
        if not checktarget:
            checktarget = 'total'
    elif moduletocheck.lower() not in bot.privileges[channel.lower()]:
        if checktarget:
            if checktarget == 'channel':
                usagefor = trigger.sender
            else:
                usagefor = checktarget
        elif not checktarget:
            usagefor = str(trigger.nick)
            
    count = get_botdatabase_value(bot, usagefor, moduletocheck+"usage")
    
    if querytype == 'user':
        if count == 0:
            message = str('It appears that ' + usagefor + ' has not run any commands at all.')
        elif count == 1:
            message = str(usagefor + ' has run a total of ' + str(count) + ' commands.')
        else:
            message = str(usagefor + ' has run a total of ' + str(count) + ' commands.')
    elif querytype == 'invalidmodule':
        message = str("I'm sorry, but that's not a valid module to check.")
    elif querytype == 'help':
        message = str("A wiki page for this is in progress."
    else:
        if count == 0:
            message = str('It appears that ' + usagefor + ' has not run ' + moduletocheck + ' at all.')
        elif count == 1:
            message = str(usagefor + ' has run ' + moduletocheck + ' a total of ' + str(count) + ' time.')
        else:
            message = str(usagefor + ' has run ' + moduletocheck + ' a total of ' + str(count) + ' times.')
    
    bot.say(message)
