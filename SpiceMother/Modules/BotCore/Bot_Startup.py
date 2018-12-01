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
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *

# Ensure Encoding
reload(sys)
sys.setdefaultencoding('utf-8')


@event('001')
@rule('.*')
@sopel.module.thread(True)
def real_startup(bot, trigger):

    while not len(bot.privileges.keys()) > 0:
        time.sleep(1)

    # Startup
    osd(bot, bot.privileges.keys(), 'notice', bot.nick + " is now starting. Please wait while I load my configuration.")

    startupcomplete = [bot.nick + " startup complete"]

    availablecomsnum, availablecomsfiles = 0, 0

    startupcomplete.append("There are " + str(availablecomsnum) + " commands available in " + str(availablecomsfiles) + " modules.")

    # Check for python module errors during this startup
    searchphrasefound = []
    for line in os.popen("sudo service " + bot.nick + " status").read().split('\n'):
        if "modules failed to load" in str(line) and "0 modules failed to load" not in str(line):
            searchphrase = str(line).split("]:", -1)[1].replace(" modules failed to load", "")
            searchphrasefound.append(str(searchphrase) + " module(s) failed")

    # Announce to chan, then handle some closing stuff
    osd(bot, bot.privileges.keys(), 'notice', startupcomplete)

    if searchphrasefound != []:
        searchphrasefound.insert(0, "Notice to Bot Admins: ")
        searchphrasefound.append("Run the debug command for more information.")
        osd(bot, bot.privileges.keys(), 'say', searchphrasefound)
