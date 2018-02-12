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
    string = get_trigger_arg(triggerargsarray, 0)
    instigator = trigger.nick
    if string:
        bot.say("Your " + str(string) + "s are bad, and you should feel bad!")
    else:
        bot.say("Hey " + instigator + ": your face is bad and you should feel bad!")
