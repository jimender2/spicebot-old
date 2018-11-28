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


@sopel.module.commands('dbshow')
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
    nick = spicemanip(triggerargsarray, 0)
    osd(bot, trigger.sender, 'say', "nick: " + nick)
    dbkey = spicemanip(triggerargsarray, 1)
    osd(bot, trigger.sender, 'say', "dbkey: " + dbkey)
    # dbresult = get_database_value(bot,
    # get_database_value(bot, nick, databasekey):
