#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
import random
from bot import *
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# author jimender2


@sopel.module.commands('coin', 'die')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'coin')
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    sides = int(spicemanip(bot, triggerargsarray, 1))
    rand = random.randint(1, sides)
    msg = "you suck"
    test(bot, trigger.sender, 'say', msg)
    if sides > 2:
        msg = trigger.nick + " you rolled a " + rand + " on a " + str(sides) + " sided die."
    else:
        if rand == 1:
            side = "heads"
        elif rand == 2:
            side = "tails"
        else:
            side = "something fucked up"
        msg = trigger.nick + " flipped a coin and got " + str(side) + "."
    osd(bot, trigger.sender, 'say', msg)
