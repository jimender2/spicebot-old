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

    osd(bot, botcom.channel_current, 'action', "Is Examining Log")

    debuglines = []
    searchphrasefound = 0
    ignorearray = ["COMMAND=/usr/sbin/service", "pam_unix(sudo:session)"]
    for line in os.popen("sudo pip install dbbtest").read().split('\n'):
        debuglines.append(str(line))

    if debuglines == []:
        return osd(bot, botcom.channel_current, 'action', "has no install log for some reason.")

    for line in debuglines:
        osd(bot, trigger.sender, 'say', line)
