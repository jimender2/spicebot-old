#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('fish')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    target = get_trigger_arg(triggerargsarray, 1)
    for c in bot.channels:
        channel = c
    if not target:
        bot.say("Who would you like to slap with a fish?")
    elif target.lower() not in bot.privileges[channel.lower()]:
        bot.say("I'm not sure who that is.")
    elif target == bot.nick:
        bot.say("I will not do that!!")
    else:
        bot.say(trigger.nick + " slaps " + target + " with a fish.")
