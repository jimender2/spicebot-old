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

import systemd.journal


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

    bot.say(str(main(bot, bot.nick)))
    return


def main(bot, debug):
    j = systemd.journal.Reader()
    j.seek_tail()
    j.get_previous()
    for entry in j:
        bot.say(str(entry))
    # while True:
    #    event = j.wait(-1)
    #    if event == systemd.journal.APPEND:
    #        for entry in j:
    #            bot.say(str(entry['MESSAGE']))
    #    elif debug and event == systemd.journal.NOP:
    #        bot.say("DEBUG: NOP")
    #    elif debug and event == systemd.journal.INVALIDATE:
    #        bot.say("DEBUG: INVALIDATE")
    #    elif debug:
    #        bot.say("Value Error:     " + str(event))
