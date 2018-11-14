#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
import random
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# author jimender2
# contributers dysonparkes

defaults = ["The cake", "Your face", "My life", "Everything I believe in", "Everything I stand for"]


@sopel.module.commands('lie')
def mainfunction(bot, trigger):
    """Check to confirm module is enabled."""
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    """Return "x is a lie" style comment based on input arguments."""
    input = spicemanip(bot, triggerargsarray, 0)
    if not input:
        rand = random.randint(1, 5)
        if rand == 1:
            osd(bot, trigger.sender, 'say', "That's a lie!!")
        else:
            randomthing = spicemanip(bot, defaults, 'random')
            osd(bot, trigger.sender, 'say', "%s is a lie!!" % randomthing)
    else:
        osd(bot, trigger.sender, 'say', "The " + input + " is a lie!!")
