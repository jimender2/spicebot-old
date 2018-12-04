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


@nickname_commands('uptime')
@sopel.module.thread(True)
def bot_command_hub(bot, trigger):

    if not bot_startup_requirements_met(bot, ["botdict"]):
        bot.memory["uptime"] = time.time()

    botcom = botcom_nick(bot, trigger)

    # Bots block
    if bot_check_inlist(bot, botcom.instigator, [bot.nick]):
        return

    osd(bot, botcom.channel_current, 'say', "I have been running since " + str(humanized_time(time.time() - bot.memory["uptime"])) + " ago.")
