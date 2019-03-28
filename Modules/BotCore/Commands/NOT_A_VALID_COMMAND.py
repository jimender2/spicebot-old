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
@rule('^\.|!(.*)')
@sopel.module.thread(True)
def mainfunction(bot, trigger):

    botcom = botcom_symbol_trigger(bot, trigger)

    # Bots block
    if bot_check_inlist(bot, botcom.instigator, [bot.nick]):
        return

    # does not apply to bots
    if "altbots" in bot.memory:
        if bot_check_inlist(bot, botcom.instigator, bot.memory["altbots"].keys()):
            return

    execute_main(bot, trigger, botcom)
    botdict_save(bot)


def execute_main(bot, trigger, botcom):

    # command issued, check if valid
    botcom.dotcommand = spicemanip.main(botcom.triggerargsarray, 1).lower()[1:]

    # patch for people typing "...", maybe other stuff, but this verifies that there is still a command here
    while botcom.dotcommand.startswith("."):
        botcom.dotcommand = botcom.dotcommand[1:]
    if not botcom.dotcommand:
        return

    bot.memory["botdict"]["tempvals"]['all_coms']

    # other bots
    otherbotcommands = []
    if "altbots" in bot.memory:
        for botname in bot.memory["altbots"].keys():
            if "tempvals" in bot.memory["altbots"][botname].keys():
                if "all_coms" in bot.memory["altbots"][botname]["tempvals"].keys():
                    otherbotcommands.extend(bot.memory["altbots"][botname]["tempvals"]["all_coms"])

    if botcom.dotcommand not in bot.memory["botdict"]["tempvals"]['all_coms'] and botcom.dotcommand not in otherbotcommands:
        osd(bot, botcom.instigator, 'notice', ["I don't seem to have a command for " + str(botcom.dotcommand) + "!", "If you have a suggestion for this command, you can run .feature ." + str(botcom.dotcommand), " ADD DESCRIPTION HERE!"])
