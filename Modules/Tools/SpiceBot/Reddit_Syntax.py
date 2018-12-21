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

# author deathbybandaid


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
def mainfunction(bot, trigger):

    botcom = bot_module_prerun(bot, trigger, "reddit")
    if not botcom.modulerun:
        return

    execute_main(bot, trigger, botcom)

    botdict_save(bot)


def execute_main(bot, trigger, botcom):

    botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, 'lower', 'list')

    if not bot.memory["botdict"]["tempvals"]['reddit']:
        return osd(bot, botcom.channel_current, 'say', "Reddit Functionality is not operational at the moment.")

    rclass = class_create('reddit')

    rclass.channel_current = trigger.sender

    rclass.urlinput = spicemanip(bot, botcom.triggerargsarray, 1)
    if rclass.urlinput.endswith("/"):
        searchterm = spicemanip(bot, botcom.triggerargsarray, 2)
        rclass.urlinput = str(rclass.urlinput + searchterm)
        botcom.triggerargsarray.remove(botcom.triggerargsarray[0])
        botcom.triggerargsarray.remove(botcom.triggerargsarray[0])
        botcom.triggerargsarray.insert(0, rclass.urlinput)

    urlsplit = rclass.urlinput.split("/", 1)
    rclass.urltype = spicemanip(bot, urlsplit, 1)
    rclass.urlsearch = spicemanip(bot, urlsplit, 2)
    if rclass.urltype.lower() == 'r':
        rclass.urltypetxt = 'subreddit'
    elif rclass.urltype.lower() == 'u':
        rclass.urltypetxt = 'user'
    else:
        osd(bot, rclass.channel_current, 'say', "An error has occured.")
        return

    botcom.triggerargsarray.remove(botcom.triggerargsarray[0])

    page = requests.get("https://www.reddit.com/", headers=header)
    tree = html.fromstring(page.content)
    if page.status_code != 200:
        osd(bot, rclass.channel_current, 'say', "Reddit appears to be down right now.")
        return

    # Run the command's function
    command_function_run = str('reddit_' + rclass.urltype.lower() + '(bot, botcom, rclass)')
    eval(command_function_run)


def reddit_u(bot, botcom, rclass):

    subcommand_valid = ['check']
    subcommand = spicemanip(bot, [x for x in botcom.triggerargsarray if x in subcommand_valid], 1) or 'check'

    userreal = reddit_user_exists(bot, user)
    if not userreal["exists"]:
        return osd(bot, rclass.channel_current, 'say', subredditcheck["error"])

    fulluurul = str("https://www.reddit.com/" + rclass.urltype + "/" + rclass.urlsearch)
    if subcommand == 'check':
        osd(bot, rclass.channel_current, 'say', [rclass.urlsearch + " appears to be a valid reddit " + rclass.urltypetxt + "!", fulluurul])
        return


def reddit_r(bot, botcom, rclass):

    subcommand_valid = ['check', 'hot', 'new', 'top', 'random', 'controversial', 'gilded', 'rising', 'best']
    subcommand = spicemanip(bot, [x for x in botcom.triggerargsarray if x in subcommand_valid], 1) or 'check'

    rclass.fullrurul = str("https://www.reddit.com/" + rclass.urltype + "/" + rclass.urlsearch)

    subredditcheck = reddit_subreddit_check(bot, rclass.urlsearch)
    if not subredditcheck["exists"]:
        return osd(bot, rclass.channel_current, 'say', subredditcheck["error"])

    subreddit = bot.memory["botdict"]["tempvals"]['reddit'].subreddit(rclass.urlsearch)
    if subcommand == 'check':
        dispmsg = []
        dispmsg.append("[Reddit " + rclass.urltype + "/" + rclass.urlsearch + "]")
        if subreddit.over18:
            dispmsg.append("<NSFW>")
        dispmsg.append(str(subreddit.public_description))
        dispmsg.append(rclass.fullrurul)
        osd(bot, rclass.channel_current, 'say', dispmsg)
        return

    if subcommand == 'random':
        targnum = spicemanip(bot, [x for x in botcom.triggerargsarray if str(x).isdigit()], 1) or 500
    else:
        targnum = spicemanip(bot, [x for x in botcom.triggerargsarray if str(x).isdigit()], 1) or 1
    targnum = int(targnum)

    if subcommand == 'new':
        submissions = subreddit.new(limit=targnum)
    elif subcommand == 'top':
        submissions = subreddit.top(limit=targnum)
    elif subcommand == 'hot':
        submissions = subreddit.hot(limit=targnum)
    elif subcommand == 'controversial':
        submissions = subreddit.controversial(limit=targnum)
    elif subcommand == 'gilded':
        submissions = subreddit.gilded(limit=targnum)
    elif subcommand == 'rising':
        submissions = subreddit.rising(limit=targnum)
    elif subcommand == 'random':
        submissions = subreddit.hot(limit=targnum)
    else:
        osd(bot, rclass.channel_current, 'say', "An error has occured.")
        return

    listarray = []
    for submission in submissions:
        listarray.append(submission)

    if listarray == []:
        submission = None
    elif subcommand == 'random':
        submission = listarray[randint(0, len(listarray) - 1)]
    else:
        submission = listarray[targnum - 1]

    dispmsg = []
    dispmsg.append("[Reddit " + rclass.urltype + "/" + rclass.urlsearch + " " + subcommand + "]")
    if subreddit.over18:
        dispmsg.append("<NSFW>")
    if submission:
        dispmsg.append("{" + str(submission.score) + "}")
        dispmsg.append(submission.title)
        dispmsg.append(submission.url)
    else:
        dispmsg.append("No Content Found.")
    osd(bot, rclass.channel_current, 'say', dispmsg)
