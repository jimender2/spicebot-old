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


@event('JOIN')
@rule('.*')
@sopel.module.thread(True)
def botcom_player_return(bot, trigger):

    for channel in bot.channels:
        osd(bot, channel, 'say', "JOIN " + str(trigger.args))

    return

    if "botdict" not in bot.memory:
        botdict_open(bot)

    instigator = trigger.nick

    if instigator not in bot.memory["botdict"]["tempvals"]['current_users']:
        if instigator not in bot.memory["botdict"]['tempvals']['commands'].keys() and instigator not in bot.memory["botdict"]['tempvals']['alt_commands'].keys() and instigator not in bot.memory["botdict"]['tempvals']['bots_list']:
            bot.memory["botdict"]["tempvals"]['current_users'].append(instigator)

    if instigator not in bot.memory["botdict"]["users"]['users_all']:
        bot.memory["botdict"]["users"]['users_all'].append(instigator)

    if instigator in bot.memory["botdict"]["tempvals"]['offline_users']:
        bot.memory["botdict"]["tempvals"]['offline_users'].remove(instigator)
