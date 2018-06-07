#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('zoidberg')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)

def execute_main(bot, trigger, triggerargsarray):
    string = get_trigger_arg(bot, triggerargsarray, 0)
    instigator = trigger.nick
    if string:
        if string.startswith("your ") or string.startswith("ur "):
            string = get_trigger_arg(bot,triggerargsarray, '2+')
        if string.endswith("s"):
            bot.say("Your " + str(string) + " are bad, and you should feel bad!")
        else:
            bot.say("Your " + str(string) + " is bad, and you should feel bad!")
    else:
        bot.say("Hey " + instigator + ": your face is bad and you should feel bad!")
