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
# contributers deathbybandaid

validrps = ['rock', 'paper', 'scissors']


@sopel.module.commands('rpsnew')
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
    selection = spicemanip(bot, [x.lower() for x in triggerargsarray if x.lower() in validrps], 1)
    if not selection:
        return osd(bot, trigger.sender, 'say', "Valid choices are " + spicemanip(bot, validrps, "andlist"))

    computer = spicemanip(bot, validrps, 'random')
    osd(bot, trigger.sender, 'say', bot.nick + " chooses " + computer)

    if computer == selection:
        return osd(bot, trigger.sender, 'say', "It's a draw")

    winner = whodawinner(bot, trigger, instigator, selection, computer)
    osd(bot, trigger.sender, 'say', winner + " is the winner")


def whodawinner(bot, trigger, instigator, selection, computer):
    winner = 'nobody'
    if computer == "rock":
        if selection == "paper":
            winner = trigger.nick
        elif selection == "scissors":
            winner = bot.nick
    elif computer == "paper":
        if selection == "scissors":
            winner = trigger.nick
        elif selection == "rock":
            winner = bot.nick
    elif computer == "scissors":
        if selection == "rock":
            winner = trigger.nick
        elif selection == "paper":
            winner = bot.nick
    return winner
