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
bot.nick do this
@rule('^\.(.*)')
@rule('(.*)')
"""


# TODO make sure restart and update save database
@rule('^\.(.*)')
@sopel.module.thread(True)
def mainfunctionnobeguine(bot, trigger):

    # command must start with
    if not str(trigger).startswith(tuple(['.'])):
        return

    botcom = botcom_symbol_trigger(bot, trigger)

    # Bots block
    if bot_check_inlist(bot, botcom.instigator, [bot.nick]):
        return

    execute_main(bot, trigger, botcom)
    botdict_save(bot)


def execute_main(bot, trigger, botcom):

    # command issued, check if valid
    botcom.dotcommand = spicemanip(bot, botcom.triggerargsarray, 1).lower()[1:]
    if botcom.dotcommand not in bot.memory["botdict"]["tempvals"]['dict_commands'].keys() and botcom.dotcommand not in bot.memory['botdict']['tempvals']['module_commands'].keys():
        osd(bot, botcom.channel_current, 'say', ["I don't seem to have a command for " + str(botcom.dotcommand) + "!", "If you have a suggestion for this command, you can run .feature ." + str(botcom.dotcommand), " ADD DESCRIPTION HERE!"])
