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

    # py modules
    for command in ["dbbtest"]:
        comstring = []
        dictcom = bot.memory["botdict"]["tempvals"]['module_commands'][command]
        comstring.append(command)
        dispmsg.append(comstring)

    # dict coms
    for command in ["tap"]:
        comstring = []
        dictcom = bot.memory["botdict"]["tempvals"]['dict_commands'][command]
        comstring.append(command)
        dispmsg.append(comstring)

    for comstring in dispmsg:
        osd(bot, botcom.channel_current, 'say', comstring)
