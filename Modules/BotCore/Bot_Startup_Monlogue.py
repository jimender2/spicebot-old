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


@rule('(.*)')
@sopel.module.thread(True)
def bot_dictcom_hub(bot, trigger):
    if not str(trigger).startswith(tuple(['.'])):
        return

    if "botdict_loaded" not in bot.memory:
        bot_saved_jobs_process(bot, trigger, 'bot_dictcom')
        osd(bot, trigger.nick, 'notice', "If your command is valid it will run after I finish loading my dictionary configuration.")
        return

    bot_dictcom_run(bot, trigger)
    botdict_save(bot)


@sopel.module.interval(1)  # TODO make this progress with the game
def bot_start_monologue(bot):

    if "bot_monologue" in bot.memory:
        return

    for channel in bot.channels:
        osd(bot, channel, 'notice', [bot.nick + " is now starting.", "Please wait while I finish loading my dictionary configuration."])

    # add feature for other bots unique monologue

    bot.memory["bot_monologue"] = True
