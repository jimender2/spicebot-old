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


@sopel.module.commands('thug')
def mainfunction(bot, trigger):
    """Check if module is enabled."""
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'thug')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    """Handle the main task itself."""
    instigator = trigger.nick
    target = get_trigger_arg(bot, triggerargsarray, 1) or instigator
    message = "%s didn't choose the thug life, the thug life chose %s." % (target, target)
    if target.lower() not in [u.lower() for u in bot.users]:
        message = "%s didn't choose the %s life, the %s life chose %s." % (instigator,target,target,instigator)
    onscreentext(bot,['say'],message)
