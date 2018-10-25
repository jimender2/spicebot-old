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

    debuglines = []
    for line in os.popen("sudo service SpiceLab status").read().split('\n'):
        debuglines.append(str(line))

    for line in debuglines:
        osd(bot, trigger.sender, 'say', line)


"""
@sopel.module.interval(1)
def timed_logcheck(bot):
    if "timed_logcheck" not in bot.memory:
        bot.memory["timed_logcheck"] = 1

        # Save systemd Log to file
        os.system("sudo journalctl -u " + bot.nick + " >> " + log_file_path)
        errorarray = ['Error loading']

        # Search for most recent start
        recent_log_start = 0
        search_phrase = "Welcome to Sopel. Loading modules..."
        with open(log_file_path) as f:
            line_num = 0
            for line in f:
                line = line.decode('utf-8', 'ignore')
                line_num += 1
                if search_phrase in line:
                    recent_log_start = line_num

        # Make an array of Errors
        total_loading_errors = 0
        line_num = 0
        with open(log_file_path) as fb:
            for line in fb:
                line_num += 1
                currentline = line_num
                if int(currentline) >= int(recent_log_start) and any(x in line for x in errorarray):
                    total_loading_errors += 1
        os.system("sudo rm " + log_file_path)
        if total_loading_errors >= 1:
            for channel in bot.channels:
                if total_loading_errors == 1:
                    osd(bot, channel, 'say', "Notice to Bot Admins: There was a module error upon Bot start. Run the debug command for more information.")
                else:
                    osd(bot, channel, 'say', "Notice to Bot Admins: There were " + str(total_loading_errors) + " module errors upon Bot start. Run the debug command for more information.")
"""
