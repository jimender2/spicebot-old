import sopel.module
import sys
import os
import random
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('msg', 'nick', 'attach', 'server', 'join', 'whois', 'me', 'ban')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    bot.say(trigger)
    bot.say(triggerargsarray)
    
