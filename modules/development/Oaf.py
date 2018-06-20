#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import os
import sys
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

#author jimender2

@sopel.module.commands('oaf','old')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'oaf')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)

def execute_main(bot, trigger, triggerargsarray):
    channel = trigger.sender
    instigator = trigger.nick
    oldperson = get_trigger_arg(bot,triggerargsarray,1)
    thingtheyremember = get_trigger_arg(bot,triggerargsarray,'2+')
    message = "%s is so old, they remember shit like %s" % (oldperson, thingtheyremember)

    if oldperson not in [u for u in bot.users]:
        oldperson = instigator
        thingtheyremember = get_trigger_arg(bot,triggerargsarray,'1+')
    elif not oldperson:
        message = "%s is so old they forgot how to input the fucking thing they remember." % instigator

    bot.say(message)
