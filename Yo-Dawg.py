import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.rate(120)
@sopel.module.commands('yodawg')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    if trigger.group(2):
        statement = str("Yo Dawg! I heard you liked " + trigger.group(2) + ", So I put a " + trigger.group(2) + " in/on your " + trigger.group(2) + "!!!")
        bot.say(statement)
