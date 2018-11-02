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

# valid commands settings
valid_command_prefix = ['.', '!']
valid_com_types = ['simple']  # , 'target', 'fillintheblank'

"""
bot.nick do this
"""

# TODO make sure restart and update save database


@rule('(.*)')
@sopel.module.thread(True)
def bot_command_hub(bot, trigger):

    if not str(trigger).startswith(tuple(valid_command_prefix)):
        return

    # botcom dynamic Class
    botcom = class_create('botcom')
    botcom.default = 'botcom'

    # instigator
    botcom.instigator = trigger.nick

    # channel
    botcom.channel_current = trigger.sender

    if "botdict_loaded" not in bot.memory:
        osd(bot, trigger.nick, 'notice', "Please wait while I load my dictionary configuration.")
        return

    # Bots can't run commands
    if botcom.instigator in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
        return

    # command issued, check if valid
    botcom.dotcommand = spicemanip(bot, botcom.triggerargsarray, 1).lower()[1:]
    if botcom.dotcommand not in bot.memory["botdict"]["tempvals"]['dict_commands'].keys():
        return

    # command aliases
    if "aliasfor" in bot.memory["botdict"]["tempvals"]['dict_commands'][botcom.dotcommand]:
        botcom.dotcommand = bot.memory["botdict"]["tempvals"]['dict_commands'][botcom.dotcommand]["aliasfor"]

    # remainder, if any is the new arg list
    botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+')

    # patch for people typing "...", maybe other stuff, but this verifies that there is still a command here
    if not botcom.dotcommand:
        return

    # execute function based on command type
    botcom.commandtype = bot.memory["botdict"]["tempvals"]['dict_commands'][botcom.dotcommand]["type"].lower()

    # IF "&&" is in the full input, it is treated as multiple commands, and is split
    commands_array = spicemanip(bot, botcom.triggerargsarray, "split_&&")
    if commands_array == []:
        commands_array = [[]]
    for command_split_partial in commands_array:
        botcom.triggerargsarray = spicemanip(bot, command_split_partial, 'create')

        command_function_run = str('botfunction_' + botcom.commandtype + '(bot, trigger, botcom)')
        eval(command_function_run)

    # Save open global dictionary at the end of each usage
    # botdict_save(bot)


# Simple quick replies
def botfunction_simple(bot, trigger, botcom):

    specified = None
    if str(spicemanip(bot, botcom.triggerargsarray, 1)).isdigit():
        specified = spicemanip(bot, botcom.triggerargsarray, 1)
        botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+', 'list')

    if not isinstance(bot.memory["botdict"]["tempvals"]['dict_commands'][botcom.dotcommand]["reply"], list):
        reply = bot.memory["botdict"]["tempvals"]['dict_commands'][botcom.dotcommand]["reply"]
    elif specified:
        if int(specified) > len(bot.memory["botdict"]["tempvals"]['dict_commands'][botcom.dotcommand]["reply"]):
            specified = len(bot.memory["botdict"]["tempvals"]['dict_commands'][botcom.dotcommand]["reply"])
        reply = spicemanip(bot, bot.memory["botdict"]["tempvals"]['dict_commands'][botcom.dotcommand]["reply"], specified)
    else:
        reply = spicemanip(bot, bot.memory["botdict"]["tempvals"]['dict_commands'][botcom.dotcommand]["reply"], 'random')
    osd(bot, trigger.sender, 'say', reply)
