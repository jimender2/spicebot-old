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


@event('PART')
@rule('.*')
@sopel.module.thread(True)
def botcom_player_leave(bot, trigger):
    return

    # user that triggered this event
    instigator = trigger.nick

    # Channel
    channel = trigger.args[0]

    # Part message
    if len(trigger.args) == 2:
        partmessage = trigger.args[1]
    else:
        partmessage = 'nothing'

    osd(bot, channel, 'say', str(instigator) + " parted " + str(channel) + " saying " + str(partmessage))

    return

    if "botdict" not in bot.memory:
        botdict_open(bot)

    instigator = trigger.nick

    if instigator in bot.memory["botdict"]["tempvals"]['current_users']:
        bot.memory["botdict"]["tempvals"]['current_users'].remove(instigator)

    if instigator not in bot.memory["botdict"]["tempvals"]['offline_users']:
        bot.memory["botdict"]["tempvals"]['offline_users'].append(instigator)
