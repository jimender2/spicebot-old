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


# Repo
REPO_OWNER = 'SpiceBot'
REPO_NAME = 'SpiceBot'
valid_colabs = ['zsutton92', 'josh-cunning', 'Berserkir-Wolf', 'deathbybandaid', 'thetechnerd', 'SniperClif', 'jimender2']


@sopel.module.commands('feature', 'feetcher', 'fr', 'bug', 'br', 'borked', 'issue', 'wiki')
def execute_main(bot, trigger):

    botcom = bot_module_prerun(bot, trigger)
    if not botcom.modulerun:
        return

    # determine that there is a request/report
    if botcom.triggerargsarray == []:
        return osd(bot, trigger.sender, 'say', "What feature/issue do you want to post?")

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

    # some users are not allowed to request code changes from within chat, due to abuse
    # banneduserarray = get_database_value(bot, bot.nick, 'users_blocked_github') or []  # Banned Users
    # if bot_check_inlist(bot, botcom.instigator, banneduserarray):
    #    return osd(bot, trigger.sender, 'say', "Due to abusing this module you have been banned from using it, %s" % botcom.instigator)

    # what type of request/report
    if botcom.maincom in ['feature', 'fr', 'feetcher']:
        reqreptype = 'feature'
    elif botcom.maincom in ['issue', 'bug', 'br', 'borked']:
        reqreptype = 'issue'
    elif botcom.maincom in ['wiki']:
        reqreptype = 'wiki'

    reqrepdict = github_types[reqreptype]

    # Special Handling for modules
    subtype = spicemanip(bot, botcom.triggerargsarray, 1)

    # Duel/RPG
    if subtype.lower() in ["duel", ".duel", "rpg", ".rpg", "challenge", ".challenge"]:
        reqrepdict['title'] = "DUELS/RPG: " + reqrepdict['title']
        reqrepdict['assignee'] = "deathbybandaid"

    # Casino
    elif subtype.lower() in ["gamble", ".gamble", "casino", ".casino"]:
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
    make_github_issue(bot, reqrepdict, botcom)


def make_github_issue(bot, issue, botcom):

    url = str(github_dict["url_api"] + github_dict["repo_owner"] + "/" + github_dict["repo_name"] + github_dict["url_path_issues"])
    session = requests.Session()

    try:
        session.auth = (bot.memory["botdict"]["tempvals"]['ext_conf']["github"]["username"], bot.memory["botdict"]["tempvals"]['ext_conf']["github"]["password"])
    except Exception as e:
        return osd(bot, botcom.channel_current, 'priv', "Error Using Github Credentials.")

    r = session.post(url, json.dumps(issue))
    if r.status_code == 201:
        osd(bot, botcom.channel_current, 'priv', "Successfully created " + issue['title'])
    else:
        osd(bot, botcom.channel_current, 'priv', "Could not create " + issue['title'])
        osd(bot, botcom.channel_current, 'priv', str('Response:' + r.content))