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
from fake_useragent import UserAgent
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('isupdev')
def execute_main(bot, trigger):
    checksite = trigger.group(2)
    if not checksite:
        osd(bot, trigger.sender, 'say', "please enter a site")
    else:
        ua = UserAgent()
        header = {'User-Agent': str(ua.chrome)}
        url = str('https://isitup.org/' + checksite)
        page = requests.get(url, headers=header)
        if page.status_code == 200:
            dispmsg = []
            upornot = isupparse(bot, url)
            if upornot:
                osd(bot, trigger.sender, 'say', "Looks like " + checksite + " appears to be online.")
            else:
                osd(bot, trigger.sender, 'say', "Looks like " + checksite + " appears to be offline.")


def isupparse(bot, url):
    upornot = 0
    tree = gettree(bot, url)
    newtest = str(tree.xpath('//*[@id="container"]/text()'))
    bot.say(str(newtest))
    isuptext = str(tree.xpath('//*[@id="content"]/div/div/center[2]/p/strong/text()'))
    isuptext = isuptext.replace('"]', "")
    isuptext = isuptext.replace('["', "")
    if str(isuptext) == "It's you!":
        upornot = 1
    return upornot


def gettree(bot, url):
    page = requests.get(url, headers=None)
    tree = html.fromstring(page.content)
    return tree
