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
This runs at startup to mark time of bootup
"""


@event('001')
@rule('.*')
@sopel.module.thread(True)
def bot_startup_botinf(bot, trigger):

    bot.memory["uptime"] = time.time()

    # don't run jobs if not ready
    while not bot_startup_requirements_met(bot, ["botdict", "server"]):
        pass

    bot.memory["botdict"]["tempvals"]["bot_info"] = dict()

    bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)] = dict()

    for botinf in ["nick"]:
        try:
            stringeval = str(eval("bot." + botinf))
        except Exception as e:
            stringeval = None
        bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)][botinf] = stringeval

    bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]['bot_admins'] = []
    for botadmin in bot.config.core.admins:
        if botadmin not in bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]['bot_admins']:
            bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]['bot_admins'].append(botadmin)

    bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]['bot_owners'] = []
    if str(bot.config.core.owner) not in bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]['bot_owners']:
        bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]['bot_owners'].append(str(bot.config.core.owner))

    bot.memory["botdict"]["tempvals"]["bot_info"]['config_dir'] = str("/home/spicebot/.sopel/" + str(bot.nick) + "/System-Files/Configs/" + bot.memory["botdict"]["tempvals"]['servername'] + "/")
    return
    bot.memory["botdict"]["tempvals"]["bot_info"]['config_file'] = str(bot.memory["botdict"]["tempvals"]["bot_info"]['config_dir'] + str(bot.nick) + ".cfg")
    bot.msg("#spicebottest", str(bot.memory["botdict"]["tempvals"]["bot_info"]['config_file']))

    bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]['bot_config'] = dict()

    # Read configuration
    bot.memory["botdict"]["tempvals"]['bots_list'][str(bot.nick)]['configuration'] = config_file_to_dict(bot, bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]['config_file'])

    bot_startup_requirements_set(bot, "bot_info")
