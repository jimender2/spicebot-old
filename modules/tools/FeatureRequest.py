#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
import json
import requests
import ConfigParser
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

## Creds
config = ConfigParser.ConfigParser()
config.read("/home/sopel/spicebot.conf")
USERNAME = config.get("github","username")
PASSWORD = config.get("github","password")
    
# Repo
REPO_OWNER = 'deathbybandaid'
REPO_NAME = 'SpiceBot'

@sopel.module.commands('feature','issue','wiki')
def execute_main(bot, trigger):
    maincommand = trigger.group(1)
    instigator = trigger.nick
    targetmodule = 
    inputtext = trigger.group(2)
    if maincommand == 'feature':
        labels=['Feature Request']
        title='Feature Request'
        action = " requested"
        assignee = ''
    elif maincommand == 'wiki':
        labels=['Wiki Update']
        title='Wiki Update'
        action = " requested"
        assignee = "Berserkir-Wolf"
    else:
        labels=['Issue Report']
        title='Issue Report'
        action = " found an issue"
        assignee = ''
    if not inputtext:
        bot.say("What feature/issue do you want to post?")
    if inputtext.startswith('duels') or inputtext.startswith('duel'):
        labels = labels + "DUELS: "
        assignee = "deathbybandaid"
    else:
        body = inputtext
        body = str(instigator + action + ": " + body)
        make_github_issue(bot, body, labels, title, assignee)

def make_github_issue(bot, body, labels, title, assignee):
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
        bot.say("Successfully created " + title)
    else:
        bot.say("Could not create " + title)
        bot.say(str('Response:' + r.content))
