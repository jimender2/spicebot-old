#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('nelson')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'nelson')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    instigator = trigger.nick
    target = get_trigger_arg(bot, triggerargsarray, 1)
    if not target:
        message = "Who are we laughing at?"
    elif target == instigator:
        message = "Is your self esteem really that low?"
        # switch to targetcheck?
    elif target.lower() not in [u.lower() for u in bot.users]:
        message = "I'm not sure who that is."
    elif target == bot.nick:
        message = "I like to laugh, but not at my own expense."
    else:
        message = bot.nick + " points at " + target + " and laughs."
    onscreentext(bot,['say'],message)
