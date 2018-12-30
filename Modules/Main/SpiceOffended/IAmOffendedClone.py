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

comdict = {
            "author": "deathbybandaid",
            "contributors": [],
            "description": "",
            'privs': [],
            "example": "",
            "exampleresponse": "",
            }


@sopel.module.commands('iao', 'iamoffended')
def mainfunction(bot, trigger):

    botcom = bot_module_prerun(bot, trigger)
    if not botcom.modulerun:
        return

    # make sure bot is OP
    if bot.privileges[botcom.channel_current][bot.nick.lower()] >= module.OP:
        bot.write(['KICK', botcom.channel_current, botcom.instigator], str("You can't talk like that in " + str(botcom.channel_current)))
        bot.say(botcom.instigator + " had that coming. Anybody got a problem with that?")
    else:
        bot.say("I need to be OP to kick unauthorized users such as " + trigger.nick + " from " + trigger.sender + " for being offended.")
