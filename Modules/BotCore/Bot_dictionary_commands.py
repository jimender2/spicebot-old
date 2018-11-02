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

"""
bot.nick do this
"""

# TODO make sure restart and update save database


@rule('(.*)')
@sopel.module.thread(True)
def bot_command_hub(bot, trigger):

    if not str(trigger).startswith(tuple(valid_command_prefix)):
        return

    if "botdict_loaded" not in bot.memory:
        osd(bot, trigger.nick, 'notice', "Please wait while I load my dictionary configuration.")
        return

    # botcom dynamic Class
    botcom = class_create('botcom')
    botcom.default = 'botcom'

    # instigator
    botcom.instigator = trigger.nick

    # channel
    botcom.channel_current = trigger.sender

    # Bots can't run commands
    if botcom.instigator in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
        return

    # create arg list
    botcom.triggerargsarray = spicemanip(bot, trigger, 'create')

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


# Quick replies with a target person TODO use the targetfinder logic
def botfunction_target(bot, trigger, botcom):

    # target is the first arg given
    target = spicemanip(bot, botcom.triggerargsarray, 1)

    # handling for no target
    if not target:

        specified = None
        if str(spicemanip(bot, botcom.triggerargsarray, 1)).isdigit():
            specified = spicemanip(bot, botcom.triggerargsarray, 1)
            botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+', 'list')

        # Seperate reply for no input
        if "noinputreply" in bot.memory["botdict"]["tempvals"]['dict_commands'][botcom.dotcommand].keys():
            if not isinstance(bot.memory["botdict"]["tempvals"]['dict_commands'][botcom.dotcommand]["noinputreply"], list):
                reply = bot.memory["botdict"]["tempvals"]['dict_commands'][botcom.dotcommand]["noinputreply"]
            elif specified:
                if int(specified) > len(bot.memory["botdict"]["tempvals"]['dict_commands'][botcom.dotcommand]["noinputreply"]):
                    specified = len(bot.memory["botdict"]["tempvals"]['dict_commands'][botcom.dotcommand]["noinputreply"])
                reply = spicemanip(bot, bot.memory["botdict"]["tempvals"]['dict_commands'][botcom.dotcommand]["noinputreply"], specified)
            else:
                reply = spicemanip(bot, bot.memory["botdict"]["tempvals"]['dict_commands'][botcom.dotcommand]["noinputreply"], 'random')
            return osd(bot, trigger.sender, 'say', reply)

        # backup target, usually instigator
        if "backuptarget" in bot.memory["botdict"]["tempvals"]['dict_commands'][botcom.dotcommand].keys():
            target = bot.memory["botdict"]["tempvals"]['dict_commands'][botcom.dotcommand]["backuptarget"]
            if target == 'instigator':
                target = botcom.instigator

        # still no target
        if not target and "backuptarget" not in bot.memory["botdict"]["tempvals"]['dict_commands'][botcom.dotcommand].keys():
            reply = "This command requires a target"
            return osd(bot, botcom.instigator, 'notice', reply)

    # remove target
    if target in botcom.triggerargsarray:
        botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+', 'list')

    specified = None
    if str(spicemanip(bot, botcom.triggerargsarray, 1)).isdigit():
        specified = spicemanip(bot, botcom.triggerargsarray, 1)
        botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+', 'list')

    # cannot target bots
    if target in bot.memory["botdict"]["tempvals"]['bots_list']:
        reply = nick_actual(bot, target) + " is a bot and cannot be targeted."
        return osd(bot, botcom.instigator, 'notice', reply)

    # Not a valid user
    if target not in bot.memory["botdict"]["users"].keys():
        reply = "I don't know who that is."
        return osd(bot, botcom.instigator, 'notice', reply)

    # User offline
    if target not in bot.memory["botdict"]["tempvals"]['all_current_users']:
        reply = "It looks like " + nick_actual(bot, target) + " is offline right now!"
        return osd(bot, botcom.instigator, 'notice', reply)

    if not botcom.channel_current.startswith('#') and target != botcom.instigator:
        reply = "Leave " + nick_actual(bot, target) + " out of this private conversation!"
        return osd(bot, botcom.instigator, 'notice', reply)

    if target in bot.memory["botdict"]["tempvals"]['all_current_users'] and target not in bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['current_users']:
        reply = "It looks like " + nick_actual(bot, target) + " is online right now, but in a different channel."
        return osd(bot, botcom.instigator, 'notice', reply)

    if not isinstance(bot.memory["botdict"]["tempvals"]['dict_commands'][botcom.dotcommand]["reply"], list):
        reply = bot.memory["botdict"]["tempvals"]['dict_commands'][botcom.dotcommand]["reply"]
    elif specified:
        if int(specified) > len(bot.memory["botdict"]["tempvals"]['dict_commands'][botcom.dotcommand]["reply"]):
            specified = len(bot.memory["botdict"]["tempvals"]['dict_commands'][botcom.dotcommand]["reply"])
        reply = spicemanip(bot, bot.memory["botdict"]["tempvals"]['dict_commands'][botcom.dotcommand]["reply"], specified)
    else:
        reply = spicemanip(bot, bot.memory["botdict"]["tempvals"]['dict_commands'][botcom.dotcommand]["reply"], 'random')
    reply = reply.replace("$target", target)
    osd(bot, trigger.sender, 'say', reply)
