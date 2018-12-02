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
"""


# Start listener on welcome RPL, which should only ever be received once
@event('001')
@rule('.*')
@sopel.module.thread(True)
def watch_server_connection(bot, trigger):

    while not len(bot.privileges.keys()) > 0:
        pass
    bot.msg("#spicemotherdev", "here")

    bot_startup_requirements_set(bot, "connected")
