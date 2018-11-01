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


@event('KICK')
@rule('.*')
@sopel.module.thread(True)
def botcom_player_return(bot, trigger):
    return

    # user that triggered this event
    instigator = trigger.nick

    # Channel
    channel = trigger.args[0]

    # target
    target = trigger.args[1]

    for channel in bot.channels:
        osd(bot, channel, 'say', str(target) + " was kicked from " + str(channel) + " by " + str(instigator))
