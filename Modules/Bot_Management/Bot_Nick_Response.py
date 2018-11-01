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

# valid commands that the bot will reply to by name
valid_botnick_commands = ['uptime', 'dict']


"""
bot.nick do this
"""

# TODO make sure restart and update save database


@nickname_commands('(.*)')
@sopel.module.thread(True)
def bot_command_hub(bot, trigger):
    if "botdict_loaded" not in bot.memory:
        osd(bot, trigger.nick, 'notice', "Please wait while I load my dictionary configuration.")
        return

    # botcom dynamic Class
    botcom = class_create('botcom')
    botcom.default = 'botcom'

    # instigator
    botcom.instigator = trigger.nick

    # create arg list
    botcom.triggerargsarray = spicemanip(bot, trigger, '2+', 'list')

    # IF "&&" is in the full input, it is treated as multiple commands, and is split
    commands_array = spicemanip(bot, botcom.triggerargsarray, "split_&&")
    if commands_array == []:
        commands_array = [[]]
    invalidcomslist = []
    for command_split_partial in commands_array:
        botcom.triggerargsarray = spicemanip(bot, command_split_partial, 'create')

        # Command Used
        botcom.command_main = spicemanip(bot, botcom.triggerargsarray, 1)
        if botcom.command_main.lower() not in valid_botnick_commands:
            invalidcomslist.append(botcom.command_main)
        else:

            bot_command_function_run = str('bot_command_function_' + botcom.command_main.lower() + '(bot,trigger,botcom)')
            eval(bot_command_function_run)

    # Display Invalids coms used
    if invalidcomslist != []:
        osd(bot, trigger.nick, 'notice', "I was unable to process the following Bot Nick commands: " + spicemanip(bot, invalidcomslist, 'andlist'))


"""
Uptime
"""


def bot_command_function_uptime(bot, trigger, botcom):
    delta = datetime.timedelta(seconds=round((datetime.datetime.utcnow() - bot.memory["botdict"]["tempvals"]["uptime"]).total_seconds()))
    osd(bot, trigger.sender, 'say', "I've been sitting here for {} and I keep going!".format(delta))


"""
Testing
"""


def bot_command_function_dict(bot, trigger, botcom):
    osd(bot, trigger.sender, 'say', str(bot.memory["botdict"]["users"]['users_all']))
