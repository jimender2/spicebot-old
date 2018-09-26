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


@sopel.module.commands('tbf')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'tbf')
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    myline = spicemanip(bot, triggerargsarray, 0)
    rand = random.randint(1, 10)
    i = 1
    a = ''
    while i <= rand:
        a = a + 'a'
        i = i + 1
    i = 1
    j = ''
    while i <= rand:
        j = j + 'i'
        i = i + 1
    i = 1
    h = ''
    while i <= rand:
        h = h + 'h'
        i = i + 1
    i = 1
    r = ''
    while i <= rand:
        r = r + 'r'
        i = i + 1

    fair = 'f' + a + j + h + r
    if not myline:
        message = "To be " + fair + "..."
    else:
        message = "To be " + fair + "; " + myline
    osd(bot, trigger.sender, 'say', message)
