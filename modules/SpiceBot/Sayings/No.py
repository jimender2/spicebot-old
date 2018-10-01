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


databasekey = 'obviousno'
defaultoptions = [
    "Can you trust an End User?", "Is anyone in I.T. sane?", "Is there a God?", "Can you lick your elbow?",
    "Is ice warm?", "Not at all..."]


@sopel.module.commands(
                        'no', 'nope', 'yeahnah', 'ag', 'ahneo', 'aï', 'aïlle', 'aita', 'aiwa', 'ala', 'ara', 'awa', 'bo', 'cha', 'ei', 'ez', 'hayir', 'hla', 'iié', 'illaï', 'jo', 'kadhu',
                        'kâni', 'kaore', 'laa', 'le', 'lla', 'lo', 'mba', 'na', 'nae', 'nage', 'nahániri', 'nahin', 'naï', 'nann', 'nanni', 'não', 'ne', 'né', 'nee',
                        'neen', 'nei', 'nein', 'nej', 'nem', 'neni', 'ni', 'nie', 'niet', 'non', 'nu', 'ohi', 'oya', 'rara', 'te', 'thay', 'tidak', 'tla', 'tsia',
                        'ug', 've', 'votch', 'xeyir', 'yuk')
def mainfunction(bot, trigger):
    """Check to see if the module is enabled."""
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'no')
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
