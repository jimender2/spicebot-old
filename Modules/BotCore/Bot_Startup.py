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

    while not len(bot.channels) > 0:
        time.sleep(1)

    # Startup
    for channel in bot.channels:
        osd(bot, channel, 'notice', bot.nick + " is now starting. Please wait while I load my configuration.")

    # Open Bot memory dictionary
    botdict_open(bot)

    startupcomplete = [bot.nick + " startup complete"]

    availablecomsnum, availablecomsfiles = 0, 0

    # dict commands
    availablecomsnum += len(bot.memory["botdict"]["tempvals"]['dict_commands'].keys())
    availablecomsfiles += bot.memory["botdict"]["tempvals"]['dict_module_count']

    # Module Commands
    availablecomsnum += len(bot.memory["botdict"]["tempvals"]['module_commands'].keys())
    availablecomsfiles += bot.memory["botdict"]["tempvals"]['module_count']

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

    while 'sock_port' not in bot.memory:
        time.sleep(1)
    startupcomplete.append("API Port set to " + str(bot.memory['sock_port']))

    # Announce to chan, then handle some closing stuff
    for channel in bot.channels:
        osd(bot, channel, 'notice', startupcomplete)

    if searchphrasefound != []:
        searchphrasefound.insert(0, "Notice to Bot Admins: ")
        searchphrasefound.append("Run the debug command for more information.")
        for channel in bot.channels:
            osd(bot, channel, 'say', searchphrasefound)

    stderr("Sending API registration to other bots")
    bot_register_handler_startup(bot)
    stderr("Sent API registration to other bots")

    bot_saved_jobs_run(bot)

    # iniital privacy sweep
    bot_setup_privacy_sweep(bot)
