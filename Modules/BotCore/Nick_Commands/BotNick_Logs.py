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
This is an internal logging system for the bot
"""


@nickname_commands('logs')
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

    botcom.triggerargsarray = spicemanip.main(botcom.triggerargsarray, '2+', 'list')

    logtype = spicemanip.main(botcom.triggerargsarray, 1) or None
    if not logtype or not bot_check_inlist(bot, logtype, bot.memory['logs'].keys()):
        return osd(bot, botcom.channel_current, 'action', "Current valid log(s) include: " + spicemanip.main(bot.memory['logs'].keys(), 'andlist'))

    logtype = inlist_match(bot, logtype, bot.memory['logs'].keys())

    if len(bot.memory['logs'][logtype]) == 0:
        return osd(bot, botcom.channel_current, 'action', "No logs found for " + str(logtype) + ".")
    osd(bot, botcom.channel_current, 'action', "Is Examining " + str(logtype) + " log(s).")

    for line in bot.memory['logs'][logtype]:
        osd(bot, botcom.channel_current, 'action', str(line))
