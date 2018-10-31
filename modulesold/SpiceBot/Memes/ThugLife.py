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
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    """Handle the main task itself."""
    target = spicemanip(bot, triggerargsarray, 1)
    isvalid, validmsg = targetcheck(bot, botcom, target, instigator)
    message = "%s didn't choose the thug life, the thug life chose %s." % (botcom.instigator, botcom.instigator)
    if not isvalid == 0:
        message = "%s didn't choose the %s life, the %s life chose %s." % (botcom.instigator, target, target, botcom.instigator)
    osd(bot, trigger.sender, 'say', message)
