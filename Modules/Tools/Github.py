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
def mainfunctionnobeguine(bot, trigger):

    botcom = bot_module_prerun(bot, trigger)
    if not botcom.modulerun:
        return

    if not botcom.multiruns:
        execute_main(bot, trigger, botcom)
    else:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, botcom.triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            botcom.triggerargsarray = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, botcom)

    botdict_save(bot)


def execute_main(bot, trigger, botcom):

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

    # what type of request/report
    if botcom.maincom in ['feature', 'fr', 'feetcher']:
        reqreptype = 'feature'
    elif botcom.maincom in ['issue', 'bug', 'br', 'borked']:
        reqreptype = 'issue'
    elif botcom.maincom in ['wiki']:
        reqreptype = 'wiki'
    elif botcom.maincom in ['github']:
        return github_handler(bot, botcom)

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
        issuelink = get_github_issue(bot, url)
        osd(bot, botcom.channel_current, 'priv', "Successfully created " + issue['title'])
    else:
        osd(bot, botcom.channel_current, 'priv', "Could not create " + issue['title'])
        osd(bot, botcom.channel_current, 'priv', str('Response:' + r.content))


def get_github_issue(bot, issue):

    issuelink = None

    url = str(github_dict["url_api"] + github_dict["repo_owner"] + "/" + github_dict["repo_name"] + github_dict["url_path_issues"])
    page = requests.get(url, headers=None)
    if page.status_code != 500 and page.status_code != 503:

        data = json.loads(urllib2.urlopen(url).read())
        bot.msg("#spicebottest", str(data[0]["title"]))
        bot.msg("#spicebottest", str(data[0]["body"]))
        # for i in [0, 1, 2, 3, 4, 5]:
        #    if not issuelink:
        #        if str(data[i]["title"]) == str(issue['title']) and str(data[i]["body"]) == str(issue['body']):
        #            issuelink = str(data[i]["html_url"])

    if not issuelink:
        return ''

    return issuelink
