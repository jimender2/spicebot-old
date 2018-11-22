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


@sopel.module.interval(1)  # TODO make this progress with the game
def bot_start_monologue(bot):
    return

    if "bot_monologue" in bot.memory:
        return
    bot.memory["bot_monologue"] = True

    if "bot_monologue_chans" not in bot.memory:
        bot.memory["bot_monologue_chans"] = []

    for channel in bot.channels:
        if channel not in bot.memory["bot_monologue_chans"]:
            osd(bot, channel, 'notice', bot.nick + " is now starting. Please wait while I finish loading my dictionary configuration.")
            bot.memory["bot_monologue_chans"].append(channel)

    # add feature for other bots unique monologue
