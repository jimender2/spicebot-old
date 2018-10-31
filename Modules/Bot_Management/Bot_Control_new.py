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


"""
# bot.nick do this
"""


@nickname_commands('uptime')
@sopel.module.thread(True)
def bot_command_hub(bot, trigger):
    triggerargsarray = spicemanip(bot, trigger.group(0), 'create')
    triggerargsarray = spicemanip(bot, triggerargsarray, '2+')
    triggerargsarray = spicemanip(bot, triggerargsarray, 'create')
    bot_command_process(bot, trigger, triggerargsarray)
    bot.say("done")


def bot_command_process(bot, trigger, triggerargsarray):

    # Dyno Classes
    botcom = class_create('bot')
    instigator = class_create('instigator')
    botcom.instigator = trigger.nick

    # time
    botcom.now = time.time()

    # User
    botcom = bot_command_users(bot, botcom)

    # Channels
    botcom = bot_command_channels(bot, botcom, trigger)

    # Command Used
    botcom.command_main = spicemanip(bot, triggerargsarray, 1)
    if botcom.command_main in triggerargsarray:
        triggerargsarray.remove(botcom.command_main)
    if botcom.command_main == 'help':
        botcom.command_main = 'docs'
    botcom.triggerargsarray = triggerargsarray
    bot_command_function_run = str('bot_command_function_' + botcom.command_main.lower() + '(bot,trigger,botcom,instigator)')
    eval(bot_command_function_run)


"""
uptime.py - Uptime module
Copyright 2014, Fabian Neundorf
Licensed under the Eiffel Forum License 2.

https://sopel.chat
"""


def setup(bot):
    bot.msg('deathbybandaid', "deathbybandaid")
    if "uptime" not in bot.memory:
        bot.memory["uptime"] = datetime.datetime.utcnow()


def bot_command_function_uptime(bot, trigger, botcom, instigator):
    """.uptime - Returns the uptime of Sopel."""
    delta = datetime.timedelta(seconds=round((datetime.datetime.utcnow() -
                                              bot.memory["uptime"])
                                             .total_seconds()))
    osd(bot, trigger.sender, 'say', "I've been sitting here for {} and I keep going!".format(delta))
