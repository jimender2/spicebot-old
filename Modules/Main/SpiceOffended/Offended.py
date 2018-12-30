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


@rule('(.*)')
@sopel.module.thread(True)
def offensedetect(bot, trigger):

    # don't run jobs if not ready
    while not bot_startup_requirements_met(bot, ["botdict", "monologue"]):
        pass

    if bot_check_inlist(bot, trigger.nick, [bot.nick]):
        return

    # does not apply to bots
    if "altbots" in bot.memory:
        if bot_check_inlist(bot, trigger.nick, bot.memory["altbots"].keys()):
            return

    triggerargsarray = spicemanip(bot, trigger, 'create')
    for x in triggerargsarray:
        stringx = x.lower()

        for r in (("?", ""), ("!", ""), (".", "")):
            stringx = stringx.replace(*r)

        if stringx in ['offend', 'offended', 'offense', 'offensive']:

            # make sure bot is OP
            if bot.privileges[trigger.sender.lower()][bot.nick.lower()] >= module.OP:
                bot.write(['KICK', trigger.sender, trigger.nick], "You can't talk like that in " + trigger.sender)
            else:
                bot.say("I need to be OP to kick unauthorized users such as " + trigger.nick + " from " + trigger.sender + " for being offended.")
