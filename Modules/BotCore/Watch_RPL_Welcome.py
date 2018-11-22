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
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *

# Ensure Encoding
reload(sys)
sys.setdefaultencoding('utf-8')


@event('001')
@rule('.*')
@sopel.module.thread(True)
def real_startup(bot, trigger):

    # Startup
    for channel in bot.channels:
        osd(bot, channel, 'notice', bot.nick + " is now starting. Please wait while I finish loading my dictionary configuration.")

    # Open Bot memory dictionary
    botdict_open(bot)

    startupcomplete = [bot.nick + " startup complete"]

    availablecomsnum = 0
    availablecomsfiles = 0

    # dict commands
    availablecomsnum += len(bot.memory["botdict"]["tempvals"]['dict_commands'].keys())
    availablecomsfiles += bot.memory["botdict"]["tempvals"]['dict_module_count']

    startupcomplete.append("There are " + str(availablecomsnum) + " commands available in " + str(availablecomsfiles) + " modules.")
    for channel in bot.channels:
        osd(bot, channel, 'notice', startupcomplete)
    bot_saved_jobs_run(bot)

    # Check for python module errors during this startup
    searchphrasefound = 0
    for line in os.popen("sudo service " + bot.nick + " status").read().split('\n'):
        if not searchphrasefound and "modules failed to load" in str(line) and "0 modules failed to load" not in str(line):
            searchphrasefound = str(line).split("]:", -1)[1]

    if searchphrasefound:
        for channel in bot.channels:
            osd(bot, channel, 'say', "Notice to Bot Admins: " + str(searchphrasefound) + ". Run the debug command for more information.")
