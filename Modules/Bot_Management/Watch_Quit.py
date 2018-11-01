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


@event('QUIT')
@rule('.*')
@sopel.module.thread(True)
def botcom_player_leave(bot, trigger):

    # user that triggered this event
    instigator = trigger.nick

    # Server
    server = bot.memory["botdict"]['tempvals']['server']

    # Channel
    # channel = trigger.args[0]

    # Quit message
    if len(trigger.args) == 1:
        quitmessage = trigger.args[0]
    else:
        quitmessage = 'nothing'

    for channel in bot.channels:  # TODO channel needs to just be ones the user was active in
        osd(bot, channel, 'say', str(instigator) + " quit " + str(server) + " saying " + str(quitmessage))

    return

    if "botdict" not in bot.memory:
        botdict_open(bot)

    instigator = trigger.nick

    if instigator in bot.memory["botdict"]["tempvals"]['current_users']:
        bot.memory["botdict"]["tempvals"]['current_users'].remove(instigator)

    if instigator not in bot.memory["botdict"]["tempvals"]['offline_users']:
        bot.memory["botdict"]["tempvals"]['offline_users'].append(instigator)
