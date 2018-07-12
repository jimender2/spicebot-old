#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('trust')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    target = get_trigger_arg(bot, triggerargsarray, 0)
    if not target:
        bot.say("Trust Doesn't Rust.")
    elif target == bot.nick:
        bot.say("Why don't you trust me?")
    else:
        bot.say("I just can't ever bring myself to trust " + target + " again. I can never forgive " + target + " for the death of my boy.")
