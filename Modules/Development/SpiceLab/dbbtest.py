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

import subprocess
import json


import textwrap
import collections


@sopel.module.commands('dbbtest', 'dbbtesta')
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

    bot_visible_coms = []
    for cmds in bot.command_groups.keys():
        bot_visible_coms.append(cmds)
    bot.say(str(bot_visible_coms))

    bot_visible_coms = []
    for cmds in bot.command_groups.items():
        bot_visible_coms.append(cmds)
    bot.say(str(bot_visible_coms))

    return

    msgs = []
    name_length = max(6, max(len(k) for k in bot.command_groups.keys()))
    for category, cmds in collections.OrderedDict(sorted(bot.command_groups.items())).items():
        category = category.upper().ljust(name_length)
        cmds = set(cmds)  # remove duplicates
        cmds = '  '.join(cmds)
        msg = category + '  ' + cmds
        indent = ' ' * (name_length + 2)
        # Honestly not sure why this is a list here
        msgs.append('\n'.join(textwrap.wrap(msg, subsequent_indent=indent)))

    # bot.say(str(type("fart")))

    # for i in range(1, 6):
    #    bot.say(str(i))
