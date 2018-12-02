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
This runs at startup to mark time of bootup
"""


@event('001')
@rule('.*')
@sopel.module.thread(True)
def bot_startup_uptime(bot, trigger):

    bot.memory["uptime"] = time.time()

    while not bot_startup_requirements_met(bot, ["botdict"]):
        pass

    bot.memory["tempvals"]["uptime"] = bot.memory["uptime"]

    bot_startup_requirements_set(bot, "uptime")
