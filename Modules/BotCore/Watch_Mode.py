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

mode_dict_alias = {
                    "+o": "OP", "-o": "deOP",
                    "+v": "VOICE", "-v": "deVOICE",
                    "+h": "HOP", "-h": "deHOP",
                    "+a": "ADMIN", "-a": "deADMIN",
                    "+q": "OWNER", "-q": "deOWNER",
                    "+b": "BAN", "-b": "unBAN",
                    "+c": "noCOLOR", "-c": "COLOR",
                    #  TODO add more user/channel modes
                    }


@event('MODE')
@rule('.*')
@sopel.module.thread(True)
def botcom_player_return(bot, trigger):

    if "botdict_loaded" not in bot.memory:
        if trigger.nick != bot.nick:
            bot_saved_jobs_process(bot, trigger, 'bot_watch_mode')
        return

    bot_watch_mode_run(bot, trigger)
