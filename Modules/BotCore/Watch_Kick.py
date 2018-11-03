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


@event('KICK')
@rule('.*')
@sopel.module.thread(True)
def botcom_player_return(bot, trigger):

    if "botdict_loaded" not in bot.memory:
        bot_saved_jobs_process(bot, trigger, 'bot_kick')
        return

    bot_kick_run(bot, trigger)
