#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import os
import sopel.module
import sys
import time
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('unclear')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'unclear')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    message = "Instructions unclear, dick stuck in ceiling fan."
    osd(bot, trigger.sender, 'say', message)
