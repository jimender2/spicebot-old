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
                    }


@event('MODE')
@rule('.*')
@sopel.module.thread(True)
def botcom_player_return(bot, trigger):
    global mode_dict_alias

    #try:
    #    modeused = mode_dict_alias[trigger.args[1]]
    #except KEYERROR:
    #    modeused = trigger.args[1]
    modeused = mode_dict_alias[trigger.args[1]]

    for channel in bot.channels:
        osd(bot, channel, 'say', str(trigger.nick) + " set mode " + str(modeused) + " on " + str(trigger.args[-1]) + " in " + str(trigger.args[0]))
