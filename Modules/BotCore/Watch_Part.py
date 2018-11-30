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


@event('PART')
@rule('.*')
@sopel.module.thread(True)
def botcom_player_leave(bot, trigger):

    # don't run jobs if not ready
    while "botdict_loaded" not in bot.memory:
        time.sleep(1)

    bot_watch_part_run(bot, trigger)
