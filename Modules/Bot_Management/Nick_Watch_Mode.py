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

mode_dict_alias = {
                    "+o": "OP",
                    "-o": "deOP",
                    "+v": "VOICE",
                    "-v": "deVOICE",
                    "+h": "HOP",
                    "-h": "deHOP",
                    }


@event('MODE')
@rule('.*')
@sopel.module.thread(True)
def botcom_player_return(bot, trigger):

    if len(trigger.args) == 2:
        modetarget = "channel"
    elif len(trigger.args) == 3:
        modetarget = "user"
    else:
        for channel in bot.channels:
            osd(bot, channel, 'say', str(trigger.args))
        return

    # user that triggered this event
    instigator = trigger.nick

    # Channel mode was set
    channel = trigger.args[0]

    # Ger Mode Used
    global mode_dict_alias
    try:
        modeused = mode_dict_alias[trigger.args[1]]
    except KeyError:
        modeused = trigger.args[1]

    # target user
    if modetarget == "user":
        target = trigger.args[-1]
        osd(bot, channel, 'say', str(instigator) + " set " + str(modetarget) + " mode " + str(modeused) + " on " + str(target) + " in " + str(channel))
    elif modetarget == "channel":
        osd(bot, channel, 'say', str(instigator) + " set " + str(modetarget) + " mode " + str(modeused) + " on " + str(channel))
    else:
        for channel in bot.channels:
            osd(bot, channel, 'say', str(trigger.args))
        return
