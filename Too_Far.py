import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('toofar')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    if trigger.group(2):
        item = trigger.group(2).strip()
        if not item.endswith('ing'):
            item = str(item + "ing")
        bot.say("Only those people who risk " + str(item) + " too far, ever find out how far they can " + str(item) + "!")
