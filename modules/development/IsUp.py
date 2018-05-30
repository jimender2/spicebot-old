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

    page = requests.get(url,headers = None)
    if page.status_code == 200:
        dispmsg = []
        upornot = upparse()
        if bonus and bonus != '':
            dispmsg.append('BONUS: ' + getwebbybonus())
        onscreentext(bot, trigger.sender, dispmsg)

def upparse():
    tree = gettree()
    try:
        webbybonus = str(tree.xpath('//*[@id="primary"]/div[2]/ul/li[1]/div[2]/div[4]/div[1]/p[1]/text()'))
        #webbybonus = str(tree.xpath('//*[@id="primary"]/div/ul/li[1]/div[2]/div[2]/p/text()'))
        webbybonus = str(webbybonus.split("BONUS: ", 1)[1])
        for r in (("\\r", ""), ("\\n", ""), ("']",""), ("]",""), ('"',''), (" '","")):
            webbybonus = webbybonus.replace(*r)
        webbybonus = unicode_string_cleanup(webbybonus)
    except IndexError:
        webbybonus = ''
    return webbybonus

def gettree():
    page = requests.get(url,headers = None)
    tree= html.fromstring(page.content)
    return tree
