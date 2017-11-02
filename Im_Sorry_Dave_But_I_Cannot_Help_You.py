import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('dave')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    usernickname = trigger.nick.lower()
    if "dave" in usernickname:
        bot.say("Is that really you, Dave?")
    bot.say('Im sorry, ' + trigger.nick + ', but I cannot help you.')
