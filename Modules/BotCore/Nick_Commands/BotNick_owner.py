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


"""
This will display a link to the online wiki for the bot
"""


@nickname_commands('msg')
@sopel.module.thread(True)
def bot_command_hub(bot, trigger):

    botcom = botcom_nick(bot, trigger)

    # Bots block
    if bot_check_inlist(bot, botcom.instigator, [bot.nick]):
        return

    if not bot_nickcom_run_check(bot, botcom):
        return osd(bot, botcom.instigator, 'notice', "I was unable to process this Bot Nick command due to privilege issues.")

    currentbotsadmins = spicemanip(bot, bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]['bot_admins'], 'andlist')
    dispmsg.append(targetbot + " is owned by " + currentbotsowner)
    osd(bot, botcom.channel_current, 'say', spicemanip(bot, dispmsg, 'andlist'))
