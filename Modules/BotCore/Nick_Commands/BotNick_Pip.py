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
            'privs': ['admin', 'OP'],
            "example": "",
            "exampleresponse": "",
            }


"""
This can be utilized to install/remove python pip packages from within IRC
"""


@nickname_commands('pip')
@sopel.module.thread(True)
def bot_command_hub(bot, trigger):

    botcom = botcom_nick(bot, trigger)

    # Bots block
    if bot_check_inlist(bot, botcom.instigator, [bot.nick]):
        return

    # does not apply to bots
    if "altbots" in bot.memory:
        if bot_check_inlist(bot, botcom.instigator, bot.memory["altbots"].keys()):
            return

    if not bot_permissions_check(bot, botcom):
        return osd(bot, botcom.instigator, 'notice', "I was unable to process this Bot Nick command due to privilege issues.")

    pipcoms = ['install', 'remove']
    subcom = spicemanip(bot, [x for x in botcom.triggerargsarray if x in pipcoms], 1) or None
    if not subcom:
        return osd(bot, botcom.channel_current, 'say', "pip requires a subcommand. Valid options: " + spicemanip(bot, pipcoms, 'andlist'))

    if subcom in botcom.triggerargsarray:
        botcom.triggerargsarray.remove(subcom)

    pippackage = spicemanip(bot, botcom.triggerargsarray, 0)
    if not pippackage:
        return osd(bot, botcom.channel_current, 'say', "You must specify a pip package.")

    installines = []
    previouslysatisfied = []
    for line in os.popen("sudo pip " + str(subcom) + " " + str(pippackage)).read().split('\n'):
        if "Requirement already satisfied:" in str(line):
            packagegood = str(line).split("Requirement already satisfied:", 1)[1]
            packagegood = str(packagegood).split("in", 1)[0]
            previouslysatisfied.append(packagegood)
        else:
            installines.append(str(line))

    if previouslysatisfied != []:
        previouslysatisfiedall = spicemanip(bot, previouslysatisfied, 'andlist')
        installines.insert(0, "The following required packages have already been satisfied: " + previouslysatisfiedall)

    if installines == []:
        return osd(bot, botcom.channel_current, 'action', "has no install log for some reason.")

    for line in installines:
        osd(bot, botcom.channel_current, 'say', line)
    osd(bot, botcom.channel_current, 'say', "Possibly done.")
