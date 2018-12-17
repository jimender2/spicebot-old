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
            "contributors": ["dysonparkes", "Mace_Whatdo"],
            "description": "",
            'privs': [],
            "example": "",
            "exampleresponse": "",
            }

claimdict = {
            "fullbladderseconds": 240,
            "newbladderseconds": 200,
            }


@sopel.module.commands('claim')
def mainfunctionnobeguine(bot, trigger):

    botcom = bot_module_prerun(bot, trigger)
    if not botcom.modulerun:
        return

    botcom.multiruns = False

    if not botcom.multiruns:
        execute_main(bot, trigger, botcom)
    else:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, botcom.triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            botcom.triggerargsarray = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, botcom)

    botdict_save(bot)


def execute_main(bot, trigger, botcom):

    posstarget = spicemanip(bot, botcom.triggerargsarray, 1)
    if not posstarget:
        return osd(bot, botcom.channel_current, 'say', "Who do you want to claim?")

    if botcom.channel_priv:
        return osd(bot, botcom.instigator, 'notice', "Claims must be done in channel")

    bladderlevel = get_nick_bladder(bot, botcom, botcom.instigator)


def get_nick_bladder(bot, botcom, nick):

    # get the last timestamp of bladder usage
    bladderleveltimestamp = get_nick_value(bot, nick, "long", 'claims', "bladder") or 0
    if not bladderleveltimestamp:
        bladderleveltimestamp = time.time() - claimdict["newbladderseconds"]
        set_nick_value(bot, nick, "long", 'claims', "bladder", bladderleveltimestamp)

    # how long since last bladder expel
    timesincebladder = time.time() - bladderleveltimestamp
    bot.say(str(timesincebladder))
