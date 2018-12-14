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

    for mtype, mindex in zip(moduletypes, moduleindex):
        dictcomref = str(mtype + "_commands")
        bot.msg("#spicebottest", mtype + "    " + dictcomref)
        if mtype != 'dict':
            bot.msg("#spicebottest", str(mindex))
        else:
            bot.msg("#spicebottest", str(len(mindex)))

    moduleindex = [["dbbtest"], ["tap"], ['update'], []]
    indexcount = len(moduleindex)
    for mtype, mindex in zip(moduletypes, moduleindex):
        indexcount -= 1
        commandcount = len(mindex)

        for command in mindex:
            commandcount -= 1

            comstring = []
            dictcomref = str(mtype + "_commands")

            # command dictionary
            if command not in bot.memory["botdict"]["tempvals"][dictcomref].keys():
                bot.msg("#spicebottest", "missing com in " + str(dictcomref) + ":   " + str(command))
            dictcom = bot.memory["botdict"]["tempvals"][dictcomref][command]

            # dotcommand
            if dictcomref == 'nick_commands':
                comstring.append(str(bot.nick) + " " + command)
            else:
                comstring.append("." + command)

            # command type
            comstring.append("(" + mtype + ")")

            # and to final
            dispmsg.append(comstring)
            if (commandcount > 0 and indexcount > 0) or (indexcount == 0 and commandcount > 0):
                dispmsg.append(["     "])

    for comstring in dispmsg:
        osd(bot, botcom.channel_current, 'say', comstring)
