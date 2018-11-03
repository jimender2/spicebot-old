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
                    "+o": "OP", "-o": "deOP",
                    "+v": "VOICE", "-v": "deVOICE",
                    "+h": "HOP", "-h": "deHOP",
                    "+a": "ADMIN", "-a": "deADMIN",
                    "+q": "OWNER", "-q": "deOWNER",
                    "+b": "BAN", "-b": "unBAN",
                    "+c": "noCOLOR", "-c": "COLOR",
                    #  TODO add more user/channel modes
                    }


@event('MODE')
@rule('.*')
@sopel.module.thread(True)
def botcom_player_return(bot, trigger):

    # all we care about right now is user modes
    if len(trigger.args) < 3:
        return

    return

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
    channel = trigger.sender

    modeused = trigger.args[1]

    # target user
    target = trigger.args[-1]
    osd(bot, channel, 'say', str(instigator) + " set user mode " + str(modeused) + " on " + str(target) + " in " + str(channel))
