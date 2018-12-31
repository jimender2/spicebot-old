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
This Cycles through all of the dictionary commands
"""


@event('001')
@rule('.*')
@sopel.module.thread(True)
def bot_startup_dict_coms(bot, trigger):

    # don't run jobs if not ready
    while not bot_startup_requirements_met(bot, ["botdict", "modules", "dict_coms", 'server', "channels", "altbots"]):
        pass

    currentservername = bot.memory["botdict"]["tempvals"]['server']

    bot.memory["botdict"]["tempvals"]['all_coms'] = []

    for comtype in ['dict', 'module', 'nickname', 'rule']:
        comtypedict = str(comtype + "_commands")
        bot.memory["botdict"]["tempvals"]['all_coms'].extend(bot.memory[comtypedict].keys())

    channeldict = dict()

    for channel in bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]["channels_list"].keys():
        channeldict[str(channel).lower()] = dict()
        channeldict[str(channel).lower()]['allcoms'] = []
        channeldict[str(channel).lower()]['allcoms'].extend(bot.memory["botdict"]["tempvals"]['all_coms'])
        channeldict[str(channel).lower()]['altdibs'] = []

    for botchannel in bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]["channels_list"].keys():
        if "com_dibs" not in bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]["channels_list"][str(botchannel).lower()].keys():
            bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]["channels_list"][str(botchannel).lower()]["com_dibs"] = []
        bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]["channels_list"][str(botchannel).lower()]["com_dibs"].extend(bot.memory["botdict"]["tempvals"]['all_coms'])

    if "altbots" in bot.memory:
        for botname in bot.memory["altbots"].keys():
            if "tempvals" in bot.memory["altbots"][botname].keys():
                if "server" in bot.memory["altbots"][botname]["tempvals"].keys():
                    altbotserver = bot.memory["altbots"][botname]["tempvals"]['server']
                    if altbotserver == currentservername:
                        if "channels_list" in bot.memory["altbots"][botname]["tempvals"]["servers_list"][currentservername].keys():
                                for altbotchan in bot.memory["altbots"][botname]["tempvals"]["servers_list"][currentservername]["channels_list"].keys():
                                    if str(altbotchan).lower() in bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]["channels_list"].keys():
                                        if "com_dibs" in bot.memory["altbots"][botname]["tempvals"]["servers_list"][currentservername]["channels_list"][str(altbotchan).lower()].keys():
                                            for valcom in bot.memory["botdict"]["tempvals"]['all_coms']:
                                                if valcom in bot.memory["altbots"][botname]["tempvals"]["servers_list"][currentservername]["channels_list"][str(altbotchan).lower()]["com_dibs"]:
                                                    channeldict[str(altbotchan).lower()]['altdibs'].append(valcom)

    for channel in bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]["channels_list"].keys():
        for valcom in channeldict[str(channel).lower()]['allcoms']:
            if valcom in channeldict[str(channel).lower()]['altdibs']:
                if valcom in bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]["channels_list"][str(channel).lower()]["com_dibs"]:
                    bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]["channels_list"][str(channel).lower()]["com_dibs"].remove(valcom)
            else:
                if valcom not in bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]["channels_list"][str(channel).lower()]["com_dibs"]:
                    bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]["channels_list"][str(channel).lower()]["com_dibs"].append(valcom)

    bot_startup_requirements_set(bot, "all_coms")
