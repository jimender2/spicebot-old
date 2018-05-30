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
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

baseurl = 'https://down.com/?q='

@sopel.module.commands('isup')
def execute_main(bot, trigger):
    checksite = trigger.group(2)
    if not checksite:
        bot.say("please enter a site")
    else:
        url = str(baseurl + checksite)
        page = requests.get(url,headers = None)
        if page.status_code == 200:
            dispmsg = []
            upornot = isupparse(url)
            if upornot:
                bot.say(checksite + " appears to be up.")
            else:
                bot.say(checksite + " appears to be down.")

def isupparse(url):
    upornot = 0
    tree = gettree(url)
    isuptext = str(tree.xpath(''))
    if isuptext.startswith("It's you!"):
        upornot = 1
    return upornot

def gettree(url):
    page = requests.get(url,headers = None)
    tree= html.fromstring(page.content)
    return tree
