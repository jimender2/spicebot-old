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


@sopel.module.commands('whatitis','whatitdo')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'whatitis')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    if not trigger.group(2):
        if trigger.group(1) == 'whatitis':
            message = "What it do?"
        else:
            message = "What it is?"
        osd(bot, trigger.sender, 'say', message)
