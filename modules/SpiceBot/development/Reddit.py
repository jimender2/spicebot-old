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
import ConfigParser

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
CLIENTID = config.get("reddit", "clientid")
SECRET = config.get("reddit", "secret")

reddit = praw.Reddit(client_id=CLIENTID,
                     client_secret=SECRET,
                     user_agent='spicebot:net.example.myredditapp:v1.2.3 (by /u/SpiceBot-dbb)')


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


def execute_main(bot, trigger, triggerargsarray):

    rclass = class_create('reddit')

    rclass.channel_current = trigger.sender

    rclass.urlinput = get_trigger_arg(bot, triggerargsarray, 1)
    if rclass.urlinput.endswith("/"):
        searchterm = get_trigger_arg(bot, triggerargsarray, 2)
        rclass.urlinput = str(rclass.urlinput + searchterm)
        triggerargsarray.remove(triggerargsarray[0])
        triggerargsarray.remove(triggerargsarray[1])
        triggerargsarray.insert(0, rclass.urlinput)

    urlsplit = rclass.urlinput.split("/", 1)
    rclass.urltype = get_trigger_arg(bot, urlsplit, 1)
    rclass.urlsearch = get_trigger_arg(bot, urlsplit, 2)
    if rclass.urltype == 'r':
        rclass.urltypetxt = 'subreddit'
    elif rclass.urltype == 'u':
        rclass.urltypetxt = 'user'
    else:
        osd(bot, rclass.channel_current, 'say', "An error has occured.")
        return

    triggerargsarray.remove(triggerargsarray[0])

    page = requests.get(redditurl, headers=header)
    tree = html.fromstring(page.content)
    if page.status_code != 200:
        osd(bot, rclass.channel_current, 'say', "Reddit appears to be down right now.")
        return

    # Run the command's function
    command_function_run = str('reddit_' + rclass.urltype.lower() + '(bot, triggerargsarray, rclass)')
    eval(command_function_run)


def reddit_u(bot, triggerargsarray, rclass):
    osd(bot, rclass.channel_current, 'say', "Reddit user functionality is not available yet.")
    return


def reddit_r(bot, triggerargsarray, rclass):

    subcommand_valid = []
    subcommand = get_trigger_arg(bot, [x for x in triggerargsarray if x in subcommand_valid], 1) or 'check'

    if subcommand == 'check':


    # perform check of valid now
    subreddit = reddit.subreddit(rclass.urlsearch)
    bot.say(str(subreddit.description))

    if triggerargsarray == []:
        url = 'temp'
        osd(bot, rclass.channel_current, 'say', rclass.urlsearch + " appears to be a valid " + rclass.urltypetxt + "!")
        return
