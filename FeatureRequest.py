import sopel.module
import sys
import os
import json
import requests
import ConfigParser
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

## Creds
config = ConfigParser.ConfigParser()
config.read("/etc/spicecred.txt")
USERNAME = config.get("configuration","username")
PASSWORD = config.get("configuration","password")
    
# Repo
REPO_OWNER = 'deathbybandaid'
REPO_NAME = 'sopel-modules'

@sopel.module.commands('featurerequest')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    if not trigger.group(2):
        bot.say("What feature do you want?")
    else:
        title = str(get_trigger_arg(triggerargsarray, 0))
        make_github_issue(bot, title)

def make_github_issue(bot, title):
    body=title
    labels=['Feature Request']
    url = 'https://api.github.com/repos/%s/%s/issues' % (REPO_OWNER, REPO_NAME)
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    issue = {'title': title,
             'body': body,
             'labels': labels}
    r = session.post(url, json.dumps(issue))
    if r.status_code == 201:
        bot.say('Successfully created Issue "%s"' % title)
    else:
        bot.say('Could not create Issue "%s"' % title)
        bot.say(str('Response:' + r.content))
