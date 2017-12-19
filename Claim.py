import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('claim')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    instigator = trigger.nick
    for c in bot.channels:
        channel = c
    target = get_trigger_arg(triggerargsarray, 1)
    inchannel = trigger.sender
    if not inchannel.startswith("#"):
        bot.say("Claims must be done in channel")
    elif not target:
        bot.say("Who do you want to claim?")
    elif target == instigator:
        bot.say("You can't claim yourself!")
    elif target == bot.nick:
        bot.say("I have already been claimed by " + bot.owner +"!")
    elif target.lower() not in bot.privileges[channel.lower()]:
        bot.say("I'm not sure who that is.")
    elif trigger.nick == 'IT_Sean':
        bot.say(instigator + ' releases the contents of his bladder on ' + target + '! All should recognize this profound claim of ownership upon ' + claimed +'!')
    else:
        bot.say(instigator + ' urinates on ' + target + '! Claimed!')
