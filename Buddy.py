import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('buddy')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    if trigger.group(2):
        myline = trigger.group(2)
        if not myline.endswith('s'):
            myline = str(myline + "s")
        bot.say("let me call my buddy and get him down here... he's an expert on " + myline)
    else:
        bot.say("What is your buddy good at?")
