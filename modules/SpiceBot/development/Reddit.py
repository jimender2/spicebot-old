#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *
import praw

import requests
from fake_useragent import UserAgent
from lxml import html

# user agent and header
ua = UserAgent()
header = {'User-Agent': str(ua.chrome)}

# author deathbybandaid
redditurl = "https://www.reddit.com/"

# Creds
config = ConfigParser.ConfigParser()
config.read("/home/spicebot/spicebot.conf")
USERNAME = config.get("reddit", "username")
PASSWORD = config.get("reddit", "password")


def execute_main(bot, trigger, triggerargsarray):

    urlinput = get_trigger_arg(bot, triggerargsarray, 0)

    urlsplit = urlinput.split("/", 1)
    urltype = get_trigger_arg(bot, urlsplit, 1)
    urlsearch = get_trigger_arg(bot, urlsplit, 2)
    bot.say(str(urlsearch))
    if urltype == 'r':
        urltype = 'subreddit'
    elif urltype == 'u':
        urltype = 'user'
    else:
        osd(bot, trigger.sender, 'say', "An error has occured.")
        return

    triggerargsarray.remove(triggerargsarray[0])

    page = requests.get(redditurl, headers=header)
    tree = html.fromstring(page.content)
    if page.status_code != 200:
        osd(bot, trigger.sender, 'say', "Reddit appears to be down right now.")
        return

    # perform check of valid now

    if triggerargsarray == []:
        url = 'temp'
        osd(bot, trigger.sender, 'say', urlsearch + " appears to be a valid " + urltype + "!")
        return

    bot.say(str(triggerargsarray))
    return


@rule(r"""(?:)r/
          (
            (?:\\/ | [^/])+
          )
          """)
@rule(r"""(?:)u/
          (
            (?:\\/ | [^/])+
          )
          """)
@sopel.module.thread(True)
def mainfunctionnobeguine(bot, trigger):
    triggerargsarray = get_trigger_arg(bot, trigger.group(0), 'create')
    execute_main(bot, trigger, triggerargsarray)
