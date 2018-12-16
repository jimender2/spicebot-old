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
    while not bot_startup_requirements_met(bot, ["ext_conf", "bot_info"]):
        pass

    try:

        scopes = 'https://www.googleapis.com/auth/calendar.readonly'
        credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/spicebot/gcal.json', scopes=scopes)

    except Exception as e:
        credentials = None
        stderr("Error loading google calendar auth")
        stderr(e)

    if not credentials:
        bot.memory["botdict"]["tempvals"]['googlecal'] = None
    else:
        bot.memory["botdict"]["tempvals"]['googlecal'] = credentials

    bot_startup_requirements_set(bot, "auth_googlecal")
