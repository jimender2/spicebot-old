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
    for c in bot.channels:
        channel = c
    if not trigger.group(2):
        claimed = "new user"
    else:
        claimed = trigger.group(2).strip()
    if target == instigator:
        bot.say("You can't claim yourself!")
    elif target.lower() not in bot.privileges[channel.lower()]:
            bot.say("I'm not sure who that is.")
    if not claimed == bot.nick and not claimed == trigger.nick:
        if trigger.nick == 'IT_Sean':
            message = str(trigger.nick + ' releases the contents of his bladder on ' + claimed + '! All should recognize this profound claim of ownership upon ' + claimed +'!')
        else:
            message = str(trigger.nick + ' urinates on ' + claimed + '! Claimed!')
        bot.say(message, target)
        if target != instigator and not inchannel.startswith("#"):
                bot.notice(message, target)
