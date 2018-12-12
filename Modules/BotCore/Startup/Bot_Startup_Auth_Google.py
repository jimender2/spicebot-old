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
This reads the external config for gif api
"""


@event('001')
@rule('.*')
@sopel.module.thread(True)
def bot_startup_twitter(bot, trigger):

    # don't run jobs if not ready
    while not bot_startup_requirements_met(bot, ["ext_conf"]):
        pass

    try:
        os.system("sudo chown -R " + str(os_dict["user"]) + ":sudo /home/spicebot/gcal.json")
    except Exception as e:
        stderr("Error loading permissions on auth file")

    try:

        SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
        gcaljsonpath = '/home/spicebot/gcal.json'
        gcalstore = file.Storage(gcaljsonpath)
        gcalcreds = gcalstore.get()

        bot.memory["botdict"]["tempvals"]['google'] = build('calendar', 'v3', http=gcalcreds.authorize(Http()))

    except Exception as e:
        bot.memory["botdict"]["tempvals"]['google'] = None
        stderr("Error loading google calendar auth")

    bot_startup_requirements_set(bot, "auth_google")
