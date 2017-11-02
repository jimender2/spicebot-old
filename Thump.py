import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('thump','thumps')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    if not trigger.group(2):
        bot.say("Did you mean to thump somebody?")
    elif not trigger.group(2).strip() == bot.nick:
        bot.action('thumps ' + trigger.group(2).strip() + ' on behalf of ' + trigger.nick)
