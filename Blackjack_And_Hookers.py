import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('myown')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    myown = get_trigger_arg(triggerargsarray, 0)
    if not myown and bot.nick not in myown:
        bot.say("Fine! I'll start my own " + myown + ", with blackjack and hookers!")
