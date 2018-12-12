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

        TKEY = bot.memory["botdict"]["tempvals"]['ext_conf']["twitter"]["token"]
        TSECRET = bot.memory["botdict"]["tempvals"]['ext_conf']["twitter"]["tokensecret"]
        TTOKEN = bot.memory["botdict"]["tempvals"]['ext_conf']["twitter"]["accesstoken"]
        TTOKENSECRET = bot.memory["botdict"]["tempvals"]['ext_conf']["twitter"]["tokenaccesssecret"]

        # bot.memory["botdict"]["tempvals"]['twitter'] = twitter.Api(consumer_key=TKEY,
        #                                                           consumer_secret=TSECRET,
        #                                                           access_token_key=TTOKEN,
        #                                                           access_token_secret=TTOKENSECRET)
        bot.memory["botdict"]["tempvals"]['twitter'] = Twitter(auth=OAuth(TTOKEN, TTOKENSECRET, TKEY, TSECRET))

    except Exception as e:
        bot.memory["botdict"]["tempvals"]['twitter'] = None
        stderr("Error loading twitter auth")

    bot_startup_requirements_set(bot, "auth_twitter")
