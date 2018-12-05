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


# Creds
config = ConfigParser.ConfigParser()
config.read("/home/spicebot/spicebot.conf")
USERNAME = config.get("github", "username")
PASSWORD = config.get("github", "password")

# Repo
REPO_OWNER = 'SpiceBot'
REPO_NAME = 'SpiceBot'
valid_colabs = ['zsutton92', 'josh-cunning', 'Berserkir-Wolf', 'deathbybandaid', 'thetechnerd', 'SniperClif', 'jimender2']

# Invalid Requests
dontaskforthese = ['instakill', 'instant kill', 'random kill', 'random deaths', 'butterfingers', 'bad grenade', 'grenade failure', 'suicide', 'go off in', 'dud grenade']


@sopel.module.commands('feature', 'feetcher', 'fr', 'bug', 'br', 'borked', 'issue', 'wiki')
def execute_main(bot, trigger):

    botcom = bot_module_prerun(bot, trigger)
    if not botcom.modulerun:
        return

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

    maincommand = trigger.group(1)
    bot.say(str(botcom.triggerargsarray))

    # some users are not allowed to request code changes from within chat, due to abuse
    banneduserarray = get_database_value(bot, bot.nick, 'users_blocked_github') or []  # Banned Users
    if bot_check_inlist(bot, botcom.instigator, banneduserarray):
        return osd(bot, trigger.sender, 'say', "Due to abusing this module you have been banned from using it, %s" % botcom.instigator)

    # create array for input, determine that there is a request/report
    if botcom.triggerargsarray == []:
        return osd(bot, trigger.sender, 'say', "What feature/issue do you want to post?")

    # block request for rejected features
    for inputpart in botcom.triggerargsarray:
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
    subtype = spicemanip(bot, botcom.triggerargsarray, 1)

    # Duel/RPG
    if subtype in ["duel", ".duel", "rpg", ".rpg", "challenge", ".challenge"]:
        reqrepdict['title'] = "DUELS/RPG: " + reqrepdict['title']
        reqrepdict['assignee'] = "deathbybandaid"

    # Casino
    elif subtype in ["gamble", ".gamble", "casino", ".casino"]:
        reqrepdict['title'] = "CASINO: " + reqrepdict['title']
        reqrepdict['assignee'] = "josh-cunning"

    # possible title catch
    elif subtype.startswith("."):
        reqrepdict['title'] = reqrepdict['title'] + ": " + str(subtype)

    # manual assigning
    if not reqrepdict['assignee']:
        assignee = spicemanip(bot, [x for x in botcom.triggerargsarray if x.startswith("@")], 1) or None
        if assignee:
            assignee = str(assignee).replace("@", "")
            if assignee in valid_colabs:
                reqrepdict['assignee'] = assignee
                botcom.triggerargsarray.remove("@" + assignee)
        else:
            del reqrepdict['assignee']

    # Body text
    inputtext = spicemanip(bot, botcom.triggerargsarray, 0)
    reqrepdict['body'] = botcom.instigator + " " + reqrepdict['body'] + ": " + inputtext

    # make it happen
    make_github_issue(bot, reqrepdict, botcom.instigator)


def make_github_issue(bot, issue, botcom.instigator):
    url = 'https://api.github.com/repos/%s/%s/issues' % (REPO_OWNER, REPO_NAME)
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    r = session.post(url, json.dumps(issue))
    if r.status_code == 201:
        osd(bot, botcom.instigator, 'priv', "Successfully created " + issue['title'])
    else:
        osd(bot, botcom.instigator, 'priv', "Could not create " + issue['title'])
        osd(bot, botcom.instigator, 'priv', str('Response:' + r.content))
