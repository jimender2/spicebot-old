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
This collects all of the channel info
"""


# Start listener on welcome RPL, which should only ever be received once
@event('001')
@rule('.*')
@sopel.module.thread(True)
def bot_setup_channels(bot, trigger):

    while not bot_startup_requirements_met(bot, ["connected", "botdict", "server"]):
        pass

    currentservername = bot.memory["botdict"]["tempvals"]['server']

    # permanent
    if "channels_list" not in bot.memory["botdict"]["servers_list"][currentservername].keys():
        bot.memory["botdict"]["servers_list"][currentservername]["channels_list"] = dict()

    # temp
    bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]["channels_list"] = dict()

    for channel in bot.privileges.keys():

        # permanent listing of the channel
        if str(channel).lower() not in bot.memory["botdict"]['servers_list'][currentservername]["channels_list"].keys():
            bot.memory["botdict"]['servers_list'][currentservername]["channels_list"][str(channel).lower()] = dict()

        # temp listing of channel
        bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]['channels_list'][str(channel).lower()] = dict()

        # disabled commands per channel
        if "disabled_commands" not in bot.memory["botdict"]["servers_list"][currentservername]['channels_list'][str(channel).lower()].keys():
            bot.memory["botdict"]["servers_list"][currentservername]['channels_list'][str(channel).lower()]["disabled_commands"] = {}

        if "multirun_disabled_commands" not in bot.memory["botdict"]["servers_list"][currentservername]['channels_list'][str(channel).lower()].keys():
            bot.memory["botdict"]["servers_list"][currentservername]['channels_list'][str(channel).lower()]["multirun_disabled_commands"] = {}

        if "com_dibs" not in bot.memory["botdict"]["servers_list"][currentservername]['channels_list'][str(channel).lower()].keys():
            bot.memory["botdict"]["servers_list"][currentservername]['channels_list'][str(channel).lower()]["com_dibs"] = []

        # authorized user groups for channels
        if "auth_block" not in bot.memory["botdict"]["servers_list"][currentservername]['channels_list'][str(channel).lower()].keys():
            bot.memory["botdict"]["servers_list"][currentservername]['channels_list'][str(channel).lower()]["auth_block"] = []
        if bot.memory["botdict"]["servers_list"][currentservername]['channels_list'][str(channel).lower()]["auth_block"] == []:
            bot.memory["botdict"]["servers_list"][currentservername]['channels_list'][str(channel).lower()]["auth_block"].append("all")

    bot_startup_requirements_set(bot, "channels")
