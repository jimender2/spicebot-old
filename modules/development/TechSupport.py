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

techmessages = ["YOU MUST CONSTRUCT ADDITIONAL PYLONS!","Have you tried flinging feces at it?","Have you tried chewing the cable?","Did you try turning it off and on again?","Did you try licking the mouse? Double-lick?","Did your try replacing all the ones with zeros?"]

@sopel.module.commands('techsupport','itsupport')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    answer = get_trigger_arg(techmessages, 'random')
    bot.say(answer)
