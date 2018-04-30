#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('mccoy')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)

def execute_main(bot, trigger, triggerargsarray):
    string = get_trigger_arg(bot, triggerargsarray, '1+')
    if string:
        if string == 'doctor':
            bot.say("I don't need a doctor, damn it, I am a doctor!")
        else:
            bot.say("Dammit Jim, I'm a doctor, not a " + str(string) + "!!!")
    else:
        bot.say("He's dead, Jim.")
