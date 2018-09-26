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

# author jimender2
# contributers none


@sopel.module.commands('wargame','wargames','wg')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'wargame')
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    input = spicemanip(bot, triggerargsarray, 0)
    if input == 'play':
        osd(bot, trigger.sender, 'say', "Do you want to play thermonuclear war?")
    elif input == 'chess':
        osd(bot, trigger.sender, 'say', "Do you want to play thermonuclear war?")
    elif input == 'thermonuclear war':
        osd(bot, trigger.sender, 'say', "Wouldn't you like a good game of chess")
    else:
        osd(bot, trigger.sender, 'say', "Would you want to play a game?")
