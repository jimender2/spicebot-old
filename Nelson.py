import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('nelson')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    instigator = trigger.nick
    inchannel = trigger.sender
    if trigger.group(2):
        for c in bot.channels:
            channel = c
        target = trigger.group(2).strip()
        if target == instigator:
            bot.say('Is your self esteem really that low?')
        elif target.lower() not in bot.privileges[channel.lower()]:
            bot.say("I'm not sure who that is.")
        elif not target == bot.nick and not target == instigator:
            message = str(bot.nick + " points at " + target + " and laughs.")
            bot.say(message)
            if target != instigator and not inchannel.startswith("#"):
                bot.notice(instigator + " instructed " + message, target)
