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


"""
This is triggered after The bots startup monlogue is completed

This prompts bot admins to run the debug command for information regarding errors during startup (if any)
"""


@event('001')
@rule('.*')
@sopel.module.thread(True)
def bot_startup_errors(bot, trigger):

    # don't run jobs if not ready
    while not bot_startup_requirements_met(bot, ["botdict", "monologue"]):
        pass
    bot.msg("#spicebottest", "here")

    servicepid = str(os.popen("systemctl show " + str(bot.nick) + " --property=MainPID").read()).split("=")[-1]
    debuglines = []
    for line in os.popen(str("sudo journalctl _PID=" + str(servicepid))).read().split('\n'):
        if not str(line).startswith("-- Logs begin at"):
            line = str(line).split("Spicebot-sopel-SpiceBot ")[-1]
            if not str(line).startswith("sudo"):
                lineparts = str(line).split(": ")
                del lineparts[0]
                line = spicemanip(bot, lineparts, 0)
                debuglines.append(str(line))
        else:
            debuglines.append(str(line))

    # Check for python module errors during this startup
    searchphrasefound = []
    for line in debuglines:
        if "modules failed to load" in str(line) and "0 modules failed to load" not in str(line):
            searchphrase = str(line).split("]:", -1)[1].replace(" modules failed to load", "")
            searchphrasefound.append(str(searchphrase) + " module(s) failed")
        elif "dict files failed to load" in str(line) and "0 dict files failed to load" not in str(line):
            searchphrase = str(line).split("]:", -1)[1].replace(" dict files failed to load", "")
            searchphrasefound.append(str(searchphrase) + " dict file(s) failed")

    if searchphrasefound != []:
        searchphrasefound.insert(0, "Notice to Bot Admins: ")
        searchphrasefound.append("Run the debug command for more information.")
        osd(bot, bot.privileges.keys(), 'say', searchphrasefound)

    # Signify that startup is complete
    bot_startup_requirements_set(bot, "errors")
