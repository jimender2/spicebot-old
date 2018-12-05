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


@sopel.module.commands('isup')
def mainfunctionnobeguine(bot, trigger):

    botcom = bot_module_prerun(bot, trigger)
    if not botcom.modulerun:
        return

    execute_main(bot, trigger, botcom)

    botdict_save(bot)


def execute_main(bot, trigger, botcom):

    botcom = bot_module_prerun(bot, trigger)
    if not botcom.modulerun:
        return

    if botcom.triggerargsarray == []:
        return osd(bot, trigger.sender, 'say', "please enter a site")

    checksite = spicemanip(bot, botcom.triggerargsarray, 0)

    if str(checksite).startswith("https://"):
        checksite = checksite.replace("https://", "")
    elif str(checksite).startswith("http://"):
        checksite = checksite.replace("http://", "")

    try:
        page = requests.get("http://" + checksite, headers=header)
        tree = html.fromstring(page.content)
        statusrefurl = str("https://httpstatuses.com/" + str(page.status_code))
        osd(bot, botcom.channel_current, 'say', ["I am getting a " + str(page.status_code) + " status code for " + str(checksite), " For details, see:", statusrefurl])
    except Exception as e:
        osd(bot, botcom.channel_current, 'say', "I am unable to get a status code for " + str(checksite))
