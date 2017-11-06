import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('trying')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    if trigger.group(2):
        phrase = trigger.group(2).strip()
        if not phrase.startswith('to'):
            parta = phrase
        else:
            parta = str("to" + phrase)
        statement = str("Are you trying " + parta + "? 'Cuz that's how you " + trigger.group(2) + "!!!")
        bot.say(statement)
