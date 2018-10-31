#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import os
import sys
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


databasekey = 'maybe'
defaultoptions = ["Possibly (In wife talk: hell no)", "Lets come back to this", "Lets think about it"]


@sopel.module.commands('maybe', 'possible')
def mainfunction(bot, trigger):
    """Check to see if the module is enabled or not."""
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'maybe')
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    """Retrieve a saying for the given database key."""
    command = spicemanip(bot, triggerargsarray, 1) or 'get'
    if not sayingscheck(bot, databasekey) and command != "add":
        sayingsmodule(bot, databasekey, defaultoptions, 'initialise')
    message = sayingsmodule(bot, databasekey, triggerargsarray, command)
    osd(bot, trigger.sender, 'say', message)
