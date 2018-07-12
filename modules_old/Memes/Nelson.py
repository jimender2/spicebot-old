#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('nelson')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    instigator = trigger.nick
    target = get_trigger_arg(bot, triggerargsarray, 1)
    if not target:
        bot.say("Who are we laughing at?")
    elif target == instigator:
        bot.say('Is your self esteem really that low?')
    elif target.lower() not in [u.lower() for u in bot.users]:
        bot.say("I'm not sure who that is.")
    elif target == bot.nick:
        bot.say("I like to laugh, but not at my own expense.")
    else:
        message = str(bot.nick + " points at " + target + " and laughs.")
        bot.say(message)
