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


@sopel.module.commands('madness')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'madness')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)


def execute_main(bot, trigger, triggerargsarray):
    myline = get_trigger_arg(bot, triggerargsarray, 0)
    if not myline:
        message = "Madness? THIS—IS—SPARTA!"
    else:
        message = "Madness? THIS—IS—" + myline.upper() + "!"
    onscreentext(bot,['say'],message)
