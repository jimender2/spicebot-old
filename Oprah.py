import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.rate(120)
@sopel.module.commands('oprah')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    if trigger.group(2):
        item = trigger.group(2).strip()
        if item.startswith('a') or item.startswith('e') or item.startswith('i') or item.startswith('o') or item.startswith('u'):
            item = str('an ' + item)
        else:
            item = str('a ' + item)
        bot.say("You get " + item + "! And You get " + item + "! Everyone gets "+ item + "!")
