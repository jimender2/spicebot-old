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


comdict = {
            "author": "deathbybandaid",
            "contributors": [],
            "description": "",
            'privs': ['admin', 'OP'],
            "example": "",
            "exampleresponse": "",
            }


"""
This will pull a directory from github
"""


@nickname_commands('gitpull')
@sopel.module.thread(True)
def bot_command_hub(bot, trigger):

    botcom = botcom_nick(bot, trigger)

    # Bots block
    if bot_check_inlist(bot, botcom.instigator, [bot.nick]):
        return

    # does not apply to bots
    if "altbots" in bot.memory:
        if bot_check_inlist(bot, botcom.instigator, bot.memory["altbots"].keys()):
            return

    if not bot_permissions_check(bot, botcom):
        return osd(bot, botcom.instigator, 'notice', "I was unable to process this Bot Nick command due to privilege issues.")

    botcom.directory = get_nick_value(bot, botcom.instigator, 'temp', 'unsorted', 'current_admin_dir') or bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]["directory_main"]
    osd(bot, botcom.channel_current, 'say', "attempting to git pull " + botcom.directory)
    gitpull(bot, botcom.directory)
