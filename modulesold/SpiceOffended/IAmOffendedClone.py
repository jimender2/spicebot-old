#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# author deathbybandaid


@sopel.module.commands('iao', 'iamoffended')
def mainfunction(bot, trigger):

    # does not apply to bots
    if trigger.nick.lower() in bot_config_names(bot):
        return

    # make sure bot is OP
    if bot.privileges[trigger.sender.lower()][bot.nick.lower()] >= module.OP:
        bot.write(['KICK', trigger.sender, trigger.nick], "You can't talk like that in " + trigger.sender)
    else:
        bot.say("I need to be OP to kick unauthorized users such as " + trigger.nick + " from " + trigger.sender + " for being offended.")
