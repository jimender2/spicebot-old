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


# Automatic Run
@sopel.module.interval(60)
def autofeeds(bot):
    for feed in feeds.list:
        dispmsg = bot_dictcom_feeds_handler(bot, botcom, feed, False)
        if dispmsg != []:
            for channel in bot.privileges.keys():
                if 'feed' not in bot.memory["botdict"]['servers_list'][str(bot.memory["botdict"]["tempvals"]['server'])]['channels_list'][str(channel)]["disabled_commands"]:
                    feed_enabled = get_nick_value(bot, channel, "long", "feeds", "enabled") or []
                    if feed in feed_enabled:
                        osd(bot, channel, 'say', dispmsg)
            for user in bot.memory["botdict"]["tempvals"]["servers_list"][currentservername]['all_current_users']:
                feed_enabled = get_nick_value(bot, user, "long", "feeds", "enabled") or []
                if feed in feed_enabled:
                    osd(bot, user, 'priv', dispmsg)
