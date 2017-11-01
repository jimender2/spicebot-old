import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.rate(120)
@sopel.module.commands('sucker','suckers')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    if not trigger.group(2):
        bot.say("Who/what are for suckers??")
    else:
        myline = trigger.group(2).strip()
        if not myline.lower() == bot.nick:
            if myline.endswith('s'):
                bot.say(myline + ' are for suckers!!')
            else:
                bot.say(myline + ' is for suckers!!')
