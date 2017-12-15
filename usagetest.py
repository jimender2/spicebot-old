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
    for c in bot.channels:
        channel = c
    checktarget = get_trigger_arg(triggerargsarray, 2)
    if not checktarget:
        bot.say('No target or command')
    elif checktarget.lower() not in bot.privileges[channel.lower()] and checktarget != 'channel':
        target = instigator
        checkcmd = checktarget
    elif checktarget == 'channel':
        target = channel
        checkcmd = get_trigger_arg(triggerargsarray, 3)
    else:
        target = checktarget
        checkcmd = get_trigger_arg(triggerargsarray, 3)
    if not checkcmd:
        bot.say('what command')
    else:
        count = get_botdatabase_value(bot, usagefor, checkcmd+"usage")
        if count == 0:
            message = str('It appears that ' + usagefor + ' has not run any commands at all.')
        elif count == 1:
            message = str(usagefor + ' has run a total of ' + str(count) + ' commands.')
        else:
            message = str(usagefor + ' has run a total of ' + str(count) + ' commands.')
        if count == 0:
            message = str('It appears that ' + usagefor + ' has not run ' + moduletocheck + ' at all.')
        elif count == 1:
            message = str(usagefor + ' has run ' + moduletocheck + ' a total of ' + str(count) + ' time.')
        else:
            message = str(usagefor + ' has run ' + moduletocheck + ' a total of ' + str(count) + ' times.')
        bot.say(message)
