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


@sopel.module.interval(1)
@sopel.module.thread(True)
def initialsetup(bot):
    return
    # prevent multiple runs every second
    if "botdict_setup" in bot.memory:
        return
    bot.memory["botdict_setup"] = True
    botdict_open(bot)

    startupcomplete = [bot.nick + " startup complete"]

    availablecomsnum = 0
    availablecomsfiles = 0

    # dict commands
    availablecomsnum += len(bot.memory['dict_commands'].keys())
    availablecomsfiles += bot.memory["botdict"]["tempvals"]['dict_module_count']

    startupcomplete.append("There are " + str(availablecomsnum) + " commands available in " + str(availablecomsfiles) + " modules.")
    for channel in bot.channels:
        osd(bot, channel, 'notice', startupcomplete)
    bot_saved_jobs_run(bot)
