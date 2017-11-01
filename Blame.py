import sopel
from sopel import module, tools
import random
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.rate(120)
@sopel.module.commands('blame')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    blametargetarray = []
    channel = trigger.sender
    for u in bot.channels[channel].users:
        target = u
        disenable = get_spicebotdisenable(bot, target)
        if disenable:
            if target != instigator:
                blametargetarray.append(target)
    try:
        whotoblame =random.choice(blametargetarray)
    except IndexError:
        whotoblame = str(instigator + "'s mom")
    bot.say("It's " + whotoblame + "'s fault.")

def get_spicebotdisenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
