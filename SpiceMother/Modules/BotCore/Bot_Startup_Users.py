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

    # temp
    bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]["channels_list"] = dict()

    for channel in bot.privileges.keys():

        for checktype in ['chanops', 'chanhalfops', 'chanvoices', 'chanowners', 'chanadmins', 'current_users']:
            if checktype not in bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]['channels_list'][str(channel)].keys():
                bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]['channels_list'][str(channel)][checktype] = []

        if 'all_current_users' not in bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]['channels_list'][str(channel)].keys():
            bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]['channels_list'][str(channel)]['all_current_users'] = []

        userprivdict = dict()
        for user in bot.privileges[channel].keys():
            channel = str(channel)
            user = str(user)

            if user not in bot.memory["botdict"]["users"].keys():
                bot.memory["botdict"]["users"][user] = dict()

            if user not in bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]['channels_list'][channel]['all_current_users']:
                bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]['channels_list'][channel]['all_current_users'].append(user)

            if user not in bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]['channels_list'][channel]['current_users'] and user not in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
                bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]['channels_list'][channel]['current_users'].append(user)

            try:
                userprivdict[user] = bot.privileges[channel][user] or 0
            except KeyError:
                userprivdict[user] = 0

        for privtype in ['VOICE', 'HALFOP', 'OP', 'ADMIN', 'OWNER']:
            privstring = str("chan" + privtype.lower() + "s")
            if userprivdict[user] == eval(privtype):
                if user not in bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]['channels_list'][channel][privstring]:
                    bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]['channels_list'][channel][privstring].append(user)
            elif userprivdict[user] >= eval(privtype) and privtype == 'OWNER':
                if user not in bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]['channels_list'][channel][privstring]:
                    bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]['channels_list'][channel][privstring].append(user)
            else:
                if user in bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]['channels_list'][channel][privstring]:
                    bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]['channels_list'][channel][privstring].remove(user)

    bot_startup_requirements_set(bot, "users")
