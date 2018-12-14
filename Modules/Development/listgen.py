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
    moduletypes = ['dict', 'module', 'nickname', 'rule']
    moduleindex = []
    for comtype in moduletypes:
        comtypedict = str(comtype + "_commands")
        moduleindex.append(bot.memory["botdict"]["tempvals"][comtypedict].keys())

    # for mtype, mindex in zip(moduletypes, moduleindex):
        # bot.msg("#spicebottest", mtype + "    " + str(len(mindex)))

    moduleindex = [["tap"], ["dbbtest"], ['update'], []]
    indexcount = len(moduleindex)
    for mtype, mindex in zip(moduletypes, moduleindex):
        indexcount -= 1
        commandcount = len(mindex)

        dispmsg.append([mtype + " commands:"])

        for command in mindex:
            commandcount -= 1

            comstring = []
            dictcomref = str(mtype + "_commands")

            # command dictionary
            dictcom = bot.memory["botdict"]["tempvals"][dictcomref][str(command)]

            # dotcommand
            if dictcomref == 'nickname_commands':
                comstring.append(str(bot.nick) + " " + command)
            else:
                comstring.append("." + command)

            # and to final
            dispmsg.append(comstring)

        dispmsg.append(["     "])

    for comstring in dispmsg:
        osd(bot, botcom.channel_current, 'say', comstring)
