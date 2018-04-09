#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('drugs')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    druglocation = trigger.group(3)
    if not druglocation:
        druglocation = "somewhere tropical"
    else:
        druglocation = str("to " + druglocation)
    bot.say(trigger.nick + " contemplates selling everything and moving " + druglocation + " to sell drugs on a beach.")
