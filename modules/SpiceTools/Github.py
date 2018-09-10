#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
import json
import requests
import ConfigParser
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *
from sopel.module import ADMIN


# Creds
config = ConfigParser.ConfigParser()
config.read("/home/spicebot/spicebot.conf")
USERNAME = config.get("github", "username")
PASSWORD = config.get("github", "password")

# Repo
REPO_OWNER = 'SpiceBot'
REPO_NAME = 'SpiceBot'

# Invalid Requests
dontaskforthese = ['instakill', 'instant kill', 'random kill', 'random deaths', 'butterfingers', 'bad grenade', 'grenade failure', 'suicide', 'go off in', 'dud grenade']

github_types = {
                "feature": {
                            "labels": ['Feature Request'],
                            "title": 'Feature Request',
                            "body": "requested",
                            "assignee": False
                            },
                "issue": {
                            "labels": ['Issue Report'],
                            "title": 'Issue Report',
                            "body": "found an issue",
                            "assignee": False
                            },
                "wiki": {
                            "labels": ['Wiki Update'],
                            "title": 'Wiki Update Request',
                            "body": "requested",
                            "assignee": "Berserkir-Wolf"
                            }
}


@sopel.module.commands('feature', 'feetcher', 'fr', 'bug', 'br', 'borked', 'issue', 'wiki')
def execute_main(bot, trigger):
    maincommand = trigger.group(1)
    instigator = trigger.nick

    # some users are not allowed to request code changes from within chat, due to abuse
    banneduserarray = get_database_value(bot, bot.nick, 'users_blocked_github') or []  # Banned Users
    if instigator.lower() in [x.lower() for x in banneduserarray]:
        return osd(bot, trigger.sender, 'say', "Due to abusing this module you have been banned from using it, %s" % instigator)

    # create array for input, determine that there is a request/report
    triggerargsarray = get_trigger_arg(bot, trigger.group(2), 'create')
    inputtext = get_trigger_arg(bot, triggerargsarray, 0)
    if not inputtext:
        return osd(bot, trigger.sender, 'say', "What feature/issue do you want to post?")

    # block request for rejected features
    for inputpart in triggerargsarray:
        if inputpart.lower() in [x.lower() for x in dontaskforthese]:
            return osd(bot, trigger.sender, 'say', "That feature has already been rejected by the dev team.")

    # what type of request/report
    if maincommand in ['feature', 'fr', 'feetcher']:
        reqreptype = 'feature'
    elif maincommand in ['issue', 'bug', 'br', 'borked']:
        reqreptype = 'issue'
    elif maincommand in ['wiki']:
        reqreptype = 'wiki'

    reqrepdict = github_types[reqreptype]

    # Special Handling for modules
    subtype = get_trigger_arg(bot, triggerargsarray, 1)

    # Duel/RPG
    if subtype in ["duel", ".duel", "rpg", ".rpg", "challenge", ".challenge"]:
        reqrepdict['title'] = "DUELS/RPG: " + reqrepdict['title']
        reqrepdict['assignee'] = "deathbybandaid"

    # Casino
    elif subtype in ["gamble", ".gamble", "casino", ".casino"]:
        reqrepdict['title'] = "CASINO: " + reqrepdict['title']
        reqrepdict['assignee'] = "josh-cunning"

    # possible title catch
    if subtype.startswith("."):
        reqrepdict['title'] = reqrepdict['title'] + ": " + str(subtype)

    reqrepdict['body'] = instigator + reqrepdict['body'] + ": " + inputtext

    if not reqrepdict['assignee']:
        reqrepdict['assignee'] = get_trigger_arg(bot, [x for x in triggerargsarray if x.startswith("@")], 1) or None
        if not reqrepdict['assignee']:
            del reqrepdict['assignee']

    bot.say(str(reqrepdict))
    return

    if assignee != '':
        assignee = get_trigger_arg(bot, [x for x in trigger.group(2) if x.startswith("@")], 1) or ''
    make_github_issue(bot, body, labels, title, assignee, instigator)


def make_github_issue(bot, body, labels, title, assignee, instigator):
    url = 'https://api.github.com/repos/%s/%s/issues' % (REPO_OWNER, REPO_NAME)
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    if assignee == '':
        issue = {'title': title,
                 'body': body,
                 'labels': labels}
    else:
        issue = {'title': title,
                 'body': body,
                 'assignee': assignee,
                 'labels': labels}
    r = session.post(url, json.dumps(issue))
    if r.status_code == 201:
        osd(bot, instigator, 'priv', "Successfully created " + title)
    else:
        osd(bot, instigator, 'priv', "Could not create " + title)
        osd(bot, instigator, 'priv', str('Response:' + r.content))
