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


@sopel.module.commands('testclock')
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
    commandused = spicemanip(bot, triggerargsarray, 1)
    if commandused == 'on':
        set_database_value(bot, bot.nick, 'testclock', 1)
    elif commandused == 'off':
        set_database_value(bot, bot.nick, 'testclock', 0)
    elif commandused == 'check':
        currentsetting = get_database_value(bot, bot.nick, 'testclock')
        osd(bot, trigger.sender, 'say', str(currentsetting))


@sopel.module.interval(15)
def countdown(bot):
    currentsetting = get_database_value(bot, bot.nick, 'testclock')
    if currentsetting == 1:
        channel = '##spicebottest'
        dispmsg = '15 secs have passed'
        osd(bot, trigger.sender, 'say', dispmsg)
