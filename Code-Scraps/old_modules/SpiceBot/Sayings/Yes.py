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


databasekey = 'obviousyes'
defaultoptions = [
    "Does the Pope shit in the woods?", "Are end-users horrifyingly stupid at times?", "would dysonparkes do this https://www.youtube.com/watch?v=TtC666biAUY", "Is stupidity infectious?",
    "Is Angie a lovely woman?", "Does licking a live wire hurt?"]


@sopel.module.commands(
                    'yes', 'yep', 'yeahnahyeah', 'ae', 'ano', 'avunu', 'awo', 'aye', 'ayo', 'baht', 'bai', 'beeni', 'beli', 'cha', 'da', 'dai', 'diakh', 'ein', 'eny', 'ere', 'evet', 'ha', 'hai',
                    'han-ji', 'hoon', 'igen', 'io', 'iva', 'iya', 'ja', 'jah', 'jes', 'jo', 'ken', 'ki', 'kyllä', 'ndiyo', 'ne', 'oui', 'ova', 'ovu', 'oyi', 'po', 'sci', 'se', 'si', 'sim', 'taip',
                    'tak', 'vaer', 'vais', 'veire', 'vethe', 'waaw', 'wi', 'ya', 'yan', 'ydw', 'yea', 'yebo', 'yego', 'yo', 'yoh')
def mainfunction(bot, trigger):
    """Check to see if the module is enabled or not."""
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'yes')
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
