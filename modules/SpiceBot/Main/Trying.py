#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('trying')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    target = get_trigger_arg(bot, triggerargsarray, 1)
    phrase = get_trigger_arg(bot, triggerargsarray, '1+')
    action = get_trigger_arg(bot, triggerargsarray, '2+')
    if target:
        if target == 'to':
            parta = phrase
            partb = action
        else:
            parta = str("to " + phrase)
            partb = phrase
        statement = str("Are you trying " + parta + "? 'Cuz that's how you " + partb + "!!!")
        bot.say(statement)
    else:
        bot.say("I haven't got the faintest idea what you are trying to do.")
