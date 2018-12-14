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
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# Ensure Encoding
reload(sys)
sys.setdefaultencoding('utf-8')


"""
It then will display information to all channels regarding current boot:
    * Available Commands and how many files those commands are in
        * This includes dictionary commands, as well as python modules

When Done, marks the monolgue as complete, for other functions to be triggered
"""


@event('001')
@rule('.*')
@sopel.module.thread(True)
def bot_startup_monologue(bot, trigger):

    # don't run jobs if not ready
    while not bot_startup_requirements_met(bot, ["connected"]):
        pass

    # Startup
    osd(bot, bot.privileges.keys(), 'action', " is now starting. Please wait while I load my configuration.")

    # these are requirements to be considered "ready"
    while not bot_startup_requirements_met(bot, ["botdict", "uptime", "bot_info", "ext_conf", "server", "channels", "users", "txt_files", "auth_reddit", "ip_address", "auth_twitter", "auth_google", "feeds"]):
        pass

    startupcomplete = [bot.nick + " startup complete"]

    availablecomsnum, availablecomsfiles = 0, 0

    # dict commands
    while not bot_startup_requirements_met(bot, ["dict_coms", "modules"]):
        pass
    for comtype in ['dict', 'module', 'nickname', 'other']:
        comtypedict = str(comtype + "_commands")
        comtypecount = str(comtype + "_count")
        availablecomsnum += len(bot.memory["botdict"]["tempvals"][comtypedict].keys())
        availablecomsfiles += bot.memory["botdict"]["tempvals"][comtypecount]

    startupcomplete.append("There are " + str(availablecomsnum) + " commands available in " + str(availablecomsfiles) + " files.")

    # API port
    apiloaded = False
    if 'sock_port' in bot.memory:
        if bot.memory['sock_port']:
            apiloaded = True

    if not apiloaded:
        startupcomplete.append("API Port Not Loaded")
    else:
        startupcomplete.append("API Port set to " + str(bot.memory['sock_port']))

    while not bot_startup_requirements_met(bot, ["all_coms", "altbots"]):
        pass

    # Announce to chan, then handle some closing stuff
    osd(bot, bot.privileges.keys(), 'notice', startupcomplete)

    bot_startup_requirements_set(bot, "monologue")
