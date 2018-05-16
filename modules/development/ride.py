#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('ride')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)

def execute_main(bot, trigger, triggerargsarray):
    instigator = trigger.nick
    target = get_trigger_arg(bot, triggerargsarray, 1) or instigator
    if target == instigator:
        message = target + " wants to put on some mad max gear, drop acid, and ride a motorcycle through the desert, while listening to some CoC."
    else:
        message = target + " should put on some mad max gear, drop acid, and ride a motorcycle through the desert, while listening to some CoC."
    bot.say(message)
