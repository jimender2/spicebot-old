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


"""
This Runs at start, waits for the amount of channels to exceed 0, in the case of an IRC bouncer like ZNC

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

    startupcomplete = [bot.nick + " startup complete"]

    availablecomsnum, availablecomsfiles = 0, 0

    startupcomplete.append("There are " + str(availablecomsnum) + " commands available in " + str(availablecomsfiles) + " files.")

    # Announce to chan, then handle some closing stuff
    osd(bot, bot.privileges.keys(), 'notice', startupcomplete)

    bot_startup_requirements_set(bot, "monologue")
