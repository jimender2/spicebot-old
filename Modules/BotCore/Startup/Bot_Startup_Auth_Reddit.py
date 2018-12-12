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
def bot_startup_reddit(bot, trigger):

    # don't run jobs if not ready
    while not bot_startup_requirements_met(bot, ["ext_conf"]):
        pass

    try:

        CLIENTID = bot.memory["botdict"]["tempvals"]['ext_conf']["reddit"]["clientid"]
        SECRET = bot.memory["botdict"]["tempvals"]['ext_conf']["reddit"]["secret"]

        bot.memory["botdict"]["tempvals"]['reddit'] = praw.Reddit(
                                                                    client_id=CLIENTID,
                                                                    client_secret=SECRET,
                                                                    user_agent='spicebot:net.example.myredditapp:v1.2.3 (by /u/SpiceBot-dbb)'
                                                                    )

    except Exception as e:
        bot.memory["botdict"]["tempvals"]['reddit'] = None
        stderr("Error loading reddit auth")

    bot_startup_requirements_set(bot, "auth_reddit")
