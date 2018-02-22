#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import random
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

techmessages = ["YOU MUST CONSTRUCT ADDITIONAL PYLONS!",
                "Have you tried flinging feces at it?",
                "Have you tried chewing the cable?",
                "Did you try turning it off and on again?",
                "Did you try licking the mouse? Double-lick?",
                "Did you try replacing all the ones with zeros?",
                "Try cooling it with a jug of water.",
                "Error: Keyboard not detected. Press 'F1' to continue.",
                "Instructions unclear, dick stuck in ceiling fan."]

@sopel.module.commands('techsupport','itsupport')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    answer = get_trigger_arg(bot, techmessages, 'random')
    bot.say(answer)
