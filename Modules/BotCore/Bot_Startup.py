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

    beguineload = False
    while not beguineload:
        if len(bot.channels) > 0:
            beguineload = True
        else:
            time.sleep(1)

    # Startup
    for channel in bot.channels:
        osd(bot, channel, 'notice', bot.nick + " is now starting. Please wait while I load my configuration.")

    # Open Bot memory dictionary
    botdict_open(bot)

    startupcomplete = [bot.nick + " startup complete"]

    availablecomsnum = 0
    availablecomsfiles = 0

    # dict commands
    availablecomsnum += len(bot.memory["botdict"]["tempvals"]['dict_commands'].keys())
    availablecomsfiles += bot.memory["botdict"]["tempvals"]['dict_module_count']

    startupcomplete.append("There are " + str(availablecomsnum) + " commands available in " + str(availablecomsfiles) + " modules.")

    # Check for python module errors during this startup
    searchphrasefound = []
    for line in os.popen("sudo service " + bot.nick + " status").read().split('\n'):
        if "modules failed to load" in str(line) and "0 modules failed to load" not in str(line):
            searchphrase = str(line).split("]:", -1)[1].replace(" modules failed to load", "")
            searchphrasefound.append(str(searchphrase) + " module(s) failed")
        elif "dict files failed to load" in str(line) and "0 dict files failed to load" not in str(line):
            searchphrase = str(line).split("]:", -1)[1].replace(" dict files failed to load", "")
            searchphrasefound.append(str(searchphrase) + " dict file(s) failed")
        elif "Error loading socket on port" in str(line):
            searchphrasefound.append("Socket Port failed to load correctly")
        elif "Loaded socket on port" in str(line):
            searchphrase = str(line).split("]:", -1)[1].replace("Loaded socket on port ", "")
            startupcomplete.append("API Port set to " + str(searchphrase))

    for channel in bot.channels:
        osd(bot, channel, 'notice', startupcomplete)
    bot_saved_jobs_run(bot)

    if searchphrasefound != []:
        searchphrasefound.insert(0, "Notice to Bot Admins: ")
        searchphrasefound.append("Run the debug command for more information.")
        for channel in bot.channels:
            osd(bot, channel, 'say', searchphrasefound)
