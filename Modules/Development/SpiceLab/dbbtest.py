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


@sopel.module.commands('dbbtest')
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
