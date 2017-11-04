import sopel
from sopel import module, tools
import random
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('blame')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    if not trigger.group(2):
        blametargetarray = []
        instigator = trigger_instigator(bot, trigger)
        for c in bot.channels:
            channel = c
        for u in bot.channels[channel].users:
            target = u
            disenable = get_disenable(bot, target)
            if disenable:
                if target not instigator or target not bot.nick:
                    blametargetarray.append(target)
        try:
            whotoblame =random.choice(blametargetarray)
        except IndexError:
            whotoblame = str(instigator + "'s mom")
        bot.say("It's " + whotoblame + "'s fault.")
