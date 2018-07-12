#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import arrow
import sys
import os
import datetime
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('mgb')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)

def execute_main(bot, trigger, triggerargsarray):
    basestring = "mumble-grumble-"
    inputstring = get_trigger_arg(bot, triggerargsarray, '1+')
    displaystring = "bullshit"
    if inputstring:
        displaystring = inputstring.replace(' ','-')
    bot.say(basestring+displaystring)
