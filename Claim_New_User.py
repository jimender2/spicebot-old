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
    if not trigger.group(2):
        claimed = "new user"
    else:
        claimed = trigger.group(2).strip()
    if not claimed == bot.nick and not claimed == trigger.nick:
        if trigger.nick == 'IT_Sean':
            bot.say(trigger.nick + ' releases the contents of his bladder on ' + claimed + '! All should recognize this profound claim of ownership upon ' + claimed +'!')
        else:
            bot.say(trigger.nick + ' urinates on ' + claimed + '! Claimed!')
