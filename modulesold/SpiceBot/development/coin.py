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
    sides = spicemanip(bot, triggerargsarray, 1)
    if not sides.isdigit():
        try:
            sides = w2n.word_to_num(str(sides))
        except ValueError:
            sides = 2
    rand = random.randint(1, sides)
    if sides > 2:
        msg = trigger.sender + " you rolled a " + rand + " on a " + sides + " sided die."
    else:
        if rand == 1:
            side = "heads"
        elif rand == 2:
            side = "tails"
        else:
            side = "something fucked up"
        msg = trigger.sender + " flipped a coin and got " + side + "."
    osd(bot, trigger.sender, 'say', msg)
