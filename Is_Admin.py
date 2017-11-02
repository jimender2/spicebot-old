import sopel.module
from sopel.module import ADMIN
from sopel.tools.target import User, Channel
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.rate(120)
@sopel.module.commands('isadmin')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    target = trigger.group(3) or trigger.nick    
    if target in trigger.admin:
        bot.say(target + ' is an admin')
    else:
        bot.say(target + ' is not an admin')
