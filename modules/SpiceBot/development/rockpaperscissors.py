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
# contributers none


@sopel.module.commands('rps', 'rockpaperscissors')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'rps')
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    selection = spicemanip(bot, triggerargsarray, 1)
    selection = selection.lower()
    computer = computerChoice()
    if selection == "rock":
        test(selection, computer)
    elif selection == "rock":
        test(selection, computer)
    elif selection == "rock":
        test(selection, computer)
    else:
        osd(bot, trigger.sender, 'say', "Valid choices are rock, paper, and scissors")


def computerChoice():
    rand = random.randint(1,3)
    if rand == 1:
        choice = "rock"
    elif rand == 2:
        choice = "paper"
    elif rand == 3:
        choice = "scissors"
    else:
        choice = "Somehow I fucked this up"
    return choice
