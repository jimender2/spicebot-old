import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('wrongweek')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    if not trigger.group(2):
        item = "sniffing glue"
    else:
        item = trigger.group(2)
    bot.say("Looks like " + trigger.nick + " picked the wrong week to stop " + str(item) + "?")
