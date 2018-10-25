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
    ignorearray = ['session closed for user root', 'COMMAND=/bin/journalctl', 'COMMAND=/bin/rm', 'pam_unix(sudo:session): session opened for user root', "COMMAND=/usr/sbin/service"]
    ignorearray = ["COMMAND=/usr/sbin/service", "pam_unix(sudo:session)"]
    for line in os.popen("sudo service SpiceLab status").read().split('\n'):
        if not searchphrasefound and "Welcome to Sopel. Loading modules..." in str(line):
            searchphrasefound = 1
            bot.say("here")
        if searchphrasefound:
            if not any(x in str(line) for x in ignorearray):
                debuglines.append(str(line))

    if debuglines == []:
        return osd(bot, botcom.channel_current, 'action', "has no service log for some reason.")

    for line in debuglines:
        osd(bot, trigger.sender, 'say', line)


"""
debugloglinenumberarray = []
osd(bot, botcom.channel_current, 'action', "Is Copying Log")
os.system("sudo journalctl -u " + targetbot + " >> " + log_file_path)
osd(bot, botcom.channel_current, 'action', "Is Filtering Log")
search_phrase = "Welcome to Sopel. Loading modules..."
ignorearray = ['session closed for user root', 'COMMAND=/bin/journalctl', 'COMMAND=/bin/rm', 'pam_unix(sudo:session): session opened for user root']
mostrecentstartbot = 0
with open(log_file_path) as f:
    line_num = 0
    for line in f:
        line = line.decode('utf-8', 'ignore')
        line_num += 1
        if search_phrase in line:
            mostrecentstartbot = line_num
    line_num = 0
with open(log_file_path) as fb:
    for line in fb:
        line_num += 1
        currentline = line_num
        if int(currentline) >= int(mostrecentstartbot) and not any(x in line for x in ignorearray):
            osd(bot, botcom.channel_current, 'say', str(line))
osd(bot, botcom.channel_current, 'action', "Is Removing Log")
os.system("sudo rm " + log_file_path)
"""


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
