import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('usagetest')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    instigator = trigger.nick
    checktarget = get_trigger_arg(triggerargsarray, 2)
    if not checktarget:
        bot.say('No target or command')
    elif moduletocheck.lower() in bot.privileges[channel.lower()]:
    
    
    ## Initial ARGS of importance
    usagefor = ''
    querytype = 'specific'
    

    commandused = get_trigger_arg(triggerargsarray, 0)
    moduletocheck = get_trigger_arg(triggerargsarray, 1)
    
    for c in bot.channels:
        channel = c

    if not moduletocheck:
        querytype = 'user'
        moduletocheck = 'total'
        usagefor = str(trigger.nick)
    if moduletocheck.lower() in bot.privileges[channel.lower()]:
        querytype = 'user'
        usagefor = str(moduletocheck)
        bot.say(str(moduletocheck))
    elif moduletocheck:
        if checktarget:
            if checktarget == 'channel':
                usagefor = trigger.sender
            else:
                usagefor = checktarget
        elif not checktarget:
            usagefor = str(trigger.nick)
        
    ## get count
    count = get_botdatabase_value(bot, usagefor, moduletocheck+"usage")
    
    if querytype == 'user':
        if count == 0:
            message = str('It appears that ' + usagefor + ' has not run any commands at all.')
        elif count == 1:
            message = str(usagefor + ' has run a total of ' + str(count) + ' commands.')
        else:
            message = str(usagefor + ' has run a total of ' + str(count) + ' commands.')
    else:
        if count == 0:
            message = str('It appears that ' + usagefor + ' has not run ' + moduletocheck + ' at all.')
        elif count == 1:
            message = str(usagefor + ' has run ' + moduletocheck + ' a total of ' + str(count) + ' time.')
        else:
            message = str(usagefor + ' has run ' + moduletocheck + ' a total of ' + str(count) + ' times.')
    
    bot.say(message)
