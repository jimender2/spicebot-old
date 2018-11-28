#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel.module

# imports for system and OS access, directories
import os
import sys

# imports based on THIS file
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# Ensure Encoding
reload(sys)
sys.setdefaultencoding('utf-8')


@sopel.module.commands('argtest')
def mainfunction(bot, trigger):

    botcom = bot_module_prerun(bot, trigger)
    if not botcom.modulerun:
        return
    # IF "&&" is in the full input, it is treated as multiple commands, and is split
    commands_array = spicemanip(bot, botcom.triggerargsarray, "split_&&")
    if commands_array == []:
        commands_array = [[]]
    for command_split_partial in commands_array:
        botcom.triggerargsarray = spicemanip(bot, command_split_partial, 'create')
        execute_main(bot, trigger, botcom)


def execute_main(bot, trigger, botcom):
    arraytest = ['main']
    if isinstance(arraytest, list):
        osd(bot, trigger.sender, 'say', 'array is an array')
    else:
        osd(bot, trigger.sender, 'say', 'array is not an array')
    notarraytest = "not an array"
    if isinstance(notarraytest, list):
        osd(bot, trigger.sender, 'say', 'notarray is an array')
    else:
        osd(bot, trigger.sender, 'say', 'notarray is not an array')
    channelarray = []
    for c in bot.channels:
        channelarray.append(c)
    channel = spicemanip(channelarray, 0)
    osd(bot, trigger.sender, 'say', str(channel))
    totalarray = len(triggerargsarray)
    totalarray = totalarray + 1
    simulatedvaluearray = ['5+', '5-', '5<', '5>', 'last', '5^7', '5!', 'random', 'list']
    for i in range(0, totalarray):
        arg = spicemanip(triggerargsarray, i)
        osd(bot, trigger.sender, 'say', "arg " + str(i) + " = " + str(arg))
    for x in simulatedvaluearray:
        value = spicemanip(triggerargsarray, x)
        if value != '':
            osd(bot, trigger.sender, 'say', "arg " + str(x) + " = " + str(value))
        else:
            osd(bot, trigger.sender, 'say', "arg " + str(x) + " is empty")
