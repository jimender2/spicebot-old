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


@sopel.module.commands('listgen')
def mainfunctionnobeguine(bot, trigger):

    botcom = bot_module_prerun(bot, trigger)
    if not botcom.modulerun:
        return

    execute_main(bot, trigger, botcom)

    botdict_save(bot)


def execute_main(bot, trigger, botcom):

    bot.say("Generating a list of commands...")

    dispmsg = []
    moduletypes = ["py", "dict"]
    moduleindex = [["dbbtest"], ["tap"]]
    # moduleindex = [bot.memory["botdict"]["tempvals"]['module_commands'].keys(), bot.memory["botdict"]["tempvals"]['dict_commands'].keys()]

    for mtype, mindex in zip(moduletypes, moduleindex):

        for command in mindex:

            comstring = []

            if command in bot.memory["botdict"]["tempvals"]['module_commands'].keys():
                dictcomref = 'module_commands'
            elif command in bot.memory["botdict"]["tempvals"]['dict_commands'].keys():
                dictcomref = 'dict_commands'

            # command dictionary
            dictcom = bot.memory["botdict"]["tempvals"][dictcomref][command]

            # dotcommand
            comstring.append("." + command)

            # command type
            comstring.append("(" + mtype + ")")

            # and to final
            dispmsg.append(comstring)

    for comstring in dispmsg:
        osd(bot, botcom.channel_current, 'say', comstring)
