import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('pee','claim','urinate')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    instigator = trigger.nick
    inchannel = trigger.sender
    for c in bot.channels:
        channel = c
    if not trigger.group(2):
        target = "new user"
    else:
        target = trigger.group(2).strip()
    if target == instigator:
        bot.say("You can't claim yourself!")
    elif target.lower() not in bot.privileges[channel.lower()] and target != "new user":
            bot.say("I'm not sure who that is.")
    elif not target == bot.nick and not target == instigator:
        if trigger.nick == 'IT_Sean':
            message = str(instigator + ' releases the contents of his bladder on ' + target + '! All should recognize this profound claim of ownership upon ' + claimed +'!')
        else:
            message = str(instigator + ' urinates on ' + target + '! Claimed!')
        bot.say(message)
        if target != instigator and not inchannel.startswith("#"):
            bot.notice(message, target)
