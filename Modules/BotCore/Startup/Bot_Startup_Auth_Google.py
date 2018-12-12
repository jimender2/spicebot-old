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

    if not os.path.exists("/home/spicebot/quickstart.py"):
        stderr("Auth Program Missing, Copying")
        os.system("sudo cp " + str(bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]["directory_main"]) + "External/quickstart.py /home/spicebot/quickstart.py")
        os.system("sudo chown -R " + str(os_dict["user"]) + ":sudo /home/spicebot/quickstart.py")

    # check that auth program is there
    for line in os.popen(str("sudo python /home/spicebot/quickstart.py")):
        stderr(line)

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
