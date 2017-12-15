import sopel.module
import sys
import os
import json
import requests
import ConfigParser
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

# Authentication for user filing issue (must have read/write access to
# repository to add issue to)
USERNAME = 'SpiceBot'
#PASSWORD = ''
config = ConfigParser.ConfigParser()
config.read("/etc/spicecred.txt")
PASSWORD = config.get("configuration","password")
    
# The repository to add this issue to
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
    '''Create an issue on github.com using the given parameters.'''
    body=title
    labels=None
    # Our url to create issues via POST
    url = 'https://api.github.com/repos/%s/%s/issues' % (REPO_OWNER, REPO_NAME)
    # Create an authenticated session to create the issue
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    # Create our issue
    issue = {'title': title,
             'body': body,
             'labels': labels}
    # Add the issue to our repository
    r = session.post(url, json.dumps(issue))
    if r.status_code == 201:
        bot.say('Successfully created Issue "%s"' % title)
    else:
        bot.say('Could not create Issue "%s"' % title)
        bot.say('Response:' + r.content))
