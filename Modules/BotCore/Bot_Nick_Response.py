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
bot.nick do this
"""

# TODO make sure restart and update save database


@nickname_commands('(.*)')
@sopel.module.thread(True)
def bot_nickcom_hub(bot, trigger):

    if "botdict_loaded" not in bot.memory:
        bot_saved_jobs_process(bot, trigger, 'bot_nickcom')
        osd(bot, trigger.nick, 'notice', "If your command is valid it will run after I finish loading my dictionary configuration.")
        return

    bot_nickcom_run(bot, trigger)
    botdict_save(bot)
