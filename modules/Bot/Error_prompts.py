#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

log_path = "data/templogauto.txt"
log_file_path = os.path.join(moduledir, log_path)


def setup(bot):
    bot.msg("##spicebottest", "running")
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
            bot.msg(channel, "Notice to Bot Admins: There were " + str(total_loading_errors) + "error(s) upon Bot start. Run the debug command for more information.")
