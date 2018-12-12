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


"""
This reads the external config for gif api
"""


@event('001')
@rule('.*')
@sopel.module.thread(True)
def bot_startup_twitter(bot, trigger):

    # don't run jobs if not ready
    while not bot_startup_requirements_met(bot, ["ext_conf", "bot_info"]):
        pass

    if not os.path.exists("/home/spicebot/quickstart.py"):
        stderr("Auth Program Missing, Copying")
        os.system("sudo cp " + str(bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]["directory_main"]) + "External/quickstart.py /home/spicebot/quickstart.py")
        os.system("sudo chown -R " + str(os_dict["user"]) + ":sudo /home/spicebot/quickstart.py")

    if not os.path.exists("/home/spicebot/credentials.json"):
        stderr("Credentials File Missing, Copying")
        try:
            CLIENTID = bot.memory["botdict"]["tempvals"]['ext_conf']["google"]["clientid"]
            SECRET = bot.memory["botdict"]["tempvals"]['ext_conf']["google"]["clientsecret"]
        except Exception as e:
            bot.memory["botdict"]["tempvals"]['google'] = None
            stderr("Error loading google calendar auth")
            bot_startup_requirements_set(bot, "auth_google")
            return

        f = open("/home/spicebot/credentials.json", "w+")
        textwrite = str('{"installed":{"client_id":"' + CLIENTID + '","project_id":"spicebot-1536234792000","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://www.googleapis.com/oauth2/v3/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"' + SECRET + '","redirect_uris":["urn:ietf:wg:oauth:2.0:oob","http://localhost"]}}')
        f.write(textwrite)
        f.close()

    # sayline = True
    # for line in os.popen(str("sudo python /home/spicebot/quickstart.py --noauth_local_webserver")):
    #    if line.startswith("Traceback"):
    #        sayline = False
    #    if sayline:
    #        stderr(line)

    try:
        os.system("sudo chown -R " + str(os_dict["user"]) + ":sudo /home/spicebot/token.json")
    except Exception as e:
        stderr("Error loading permissions on auth file")

    try:

        scopes = 'https://www.googleapis.com/auth/calendar.readonly'
        credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/spicebot/token.json', scopes=scopes)
        delegated_credentials = credentials.create_delegated('spicebot@deathbybandaid.net')
        http_auth = delegated_credentials.authorize(Http())

        bot.memory["botdict"]["tempvals"]['google'] = build('calendar', 'v3', http=http_auth, cache_discovery=False)

    except Exception as e:
        bot.memory["botdict"]["tempvals"]['google'] = None
        stderr("Error loading google calendar auth")
        stderr(e)

    bot_startup_requirements_set(bot, "auth_google")
