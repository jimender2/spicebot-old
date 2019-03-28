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
        commands_array = spicemanip.main(triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip.main(command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    selection = spicemanip.main(triggerargsarray, 1)
    selection = selection.lower()
    computer = computerChoice()
    if selection == "rock":
        test(bot, trigger, instigator, selection, computer)
    elif selection == "paper":
        test(bot, trigger, instigator, selection, computer)
    elif selection == "scissors":
        test(bot, trigger, instigator, selection, computer)
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


def test(bot, trigger, instigator, selection, computer):
    osd(bot, trigger.sender, 'say', bot.nick + " chooses " + computer)
    if computer == selection:
        osd(bot, trigger.sender, 'say', "It's a draw")
    elif computer == "rock":
        if selection == "paper":
            osd(bot, trigger.sender, 'say', trigger.sender + " is the winner")
        elif selection == "scissors":
            osd(bot, trigger.sender, 'say', bot.nick + " is the winner")
    elif computer == "paper":
        if selection == "scissors":
            osd(bot, trigger.sender, 'say', trigger.sender + " is the winner")
        elif selection == "rock":
            osd(bot, trigger.sender, 'say', bot.nick + " is the winner")
    elif computer == "scissors":
        if selection == "rock":
            osd(bot, trigger.sender, 'say', trigger.sender + " is the winner")
        elif selection == "paper":
            osd(bot, trigger.sender, 'say', bot.nick + " is the winner")
    else:
        osd(bot, trigger.sender, 'say', "I fucked something up")
