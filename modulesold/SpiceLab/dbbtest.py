#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *

import subprocess
import json

validcoms = 'dbbtest', 'dbbtesta'


@sopel.module.commands('dbbtest')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    # IF "&&" is in the full input, it is treated as multiple commands, and is split
    commands_array = spicemanip(bot, triggerargsarray, "split_&&")
    if commands_array == []:
        commands_array = [[]]
    for command_split_partial in commands_array:
        triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
        execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    osd(bot, trigger.sender, 'say', "This is deathbybandaid's test module")

    bot.say(str(type("fart")))

    # for i in range(1, 6):
    #    bot.say(str(i))
