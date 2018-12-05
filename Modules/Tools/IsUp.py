#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import requests
from lxml import html
import datetime
from time import strptime
from dateutil import parser
import calendar
import arrow
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *

baseurl = 'https://down.com/?q='


@sopel.module.commands('isup')
def execute_main(bot, trigger):
    checksite = trigger.group(2)
    if not checksite:
        return osd(bot, trigger.sender, 'say', "please enter a site")

    if str(checksite).startswith("https://"):
        checksite = checksite.replace("https://", "")
    elif str(checksite).startswith("http://"):
        checksite = checksite.replace("http://", "")

    try:
        page = requests.get("http://" + checksite, headers=header)
        tree = html.fromstring(page.content)
        osd(bot, trigger.sender, 'say', "I am getting a " + str(page.status_code) + " status code for " + str(checksite))
    except Exception as e:
        osd(bot, trigger.sender, 'say', "I am unable to get a status code for " + str(checksite))
