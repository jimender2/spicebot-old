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
This makes a log of all of the users
"""


# Start listener on welcome RPL, which should only ever be received once
@event('001')
@rule('.*')
@sopel.module.thread(True)
def bot_setup_users(bot, trigger):

    while not bot_startup_requirements_met(bot, ["connected", "botdict", "server", "channels"]):
        pass

    currentservername = bot.memory["botdict"]["tempvals"]['server']

    if "users" not in bot.memory["botdict"].keys():
        bot.memory["botdict"]["users"] = dict()

    bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]['all_current_users'] = []

    for channel in bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]['channels_list'].keys():

        for checktype in ['chanops', 'chanhalfops', 'chanvoices', 'chanowners', 'chanadmins', 'current_users']:
            if checktype not in bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]['channels_list'][str(channel).lower()].keys():
                bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]['channels_list'][str(channel).lower()][checktype] = []

        userprivdict = dict()
        channelident = channel
        for identchannel in bot.privileges.keys():
            if str(identchannel).lower() == str(channel).lower():
                channelident = identchannel
        for user in bot.privileges[channelident].keys():

            if str(user) not in bot.memory["botdict"]["users"].keys():
                bot.memory["botdict"]["users"][str(user)] = dict()

            if str(user) not in bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]['all_current_users']:
                bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]['all_current_users'].append(str(user))

            if str(user) not in bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]['channels_list'][str(channel).lower()]['current_users']:
                bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]['channels_list'][str(channel).lower()]['current_users'].append(str(user))

            try:
                userprivdict[str(user)] = bot.privileges[channelident][user] or 0
            except KeyError:
                userprivdict[str(user)] = 0

            for privtype in ['VOICE', 'HALFOP', 'OP', 'ADMIN', 'OWNER']:
                privstring = str("chan" + privtype.lower() + "s")
                if userprivdict[str(user)] == eval(privtype):
                    if str(user) not in bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]['channels_list'][str(channel).lower()][privstring]:
                        bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]['channels_list'][str(channel).lower()][privstring].append(str(user))
                elif userprivdict[str(user)] >= eval(privtype) and privtype == 'OWNER':
                    if str(user) not in bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]['channels_list'][str(channel)][privstring]:
                        bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]['channels_list'][str(channel).lower()][privstring].append(str(user))
                else:
                    if str(user) in bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]['channels_list'][str(channel).lower()][privstring]:
                        bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]['channels_list'][str(channel).lower()][privstring].remove(str(user))

    bot_startup_requirements_set(bot, "users")
