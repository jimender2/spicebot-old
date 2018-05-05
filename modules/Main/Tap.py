#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
from random import randint
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('tap')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    instigator = trigger.nick
    decide = randint(1,5)
    if decide == 4:
        bot.say("FFS "+ instigator + ", of course it's bloody well on!")
    elif decide == 5:
        bot.action("clocks " + instigator + " around the head with a mic stand.")
        bot.say(instigator + ", if you do that again you'll be eating a speaker.")
    else:
        bot.say("*Tap, Tap* ...is this thing on?")
