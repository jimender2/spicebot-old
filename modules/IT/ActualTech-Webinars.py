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

url = 'https://events.actualtechmedia.com/'

@sopel.module.commands('atwebby')
def execute_main(bot, trigger):
    #webbyauto(bot)
    page = requests.get(url,headers = None)
    if page.status_code == 200:
        dispmsg = []
        dispmsg.append("[ActualTech Webinar]")
        dispmsg.append("{"+getwebbytime()+"}")
        #dispmsg.append("{"+getwebbytimeuntil()+"}")
        dispmsg.append(getwebbytitle())
        #dispmsg.append(getwebbylink())
        #dispmsg.append('BONUS: ' + getwebbybonus())
        onscreentext(bot, trigger.sender, dispmsg)

#@sopel.module.interval(60)
#def webbyauto(bot):
#    page = requests.get(url,headers = None)
#    if page.status_code == 200:
#        now = datetime.datetime.utcnow()
#        webbytime = getwebbytime()
#        timeuntil = (webbytime - now).total_seconds()
#        if int(timeuntil) < 900 and int(timeuntil) > 840:
#            dispmsg = []
#            dispmsg.append("[Spiceworks Webinar Reminder]")
#            dispmsg.append("{"+getwebbytimeuntil()+"}")
#            dispmsg.append(getwebbytitle())
#            dispmsg.append(getwebbylink())
#            dispmsg.append('BONUS: ' + getwebbybonus())
#            for channel in bot.channels:
#                onscreentext(bot, channel, dispmsg)

def getwebbytitle():
    tree = gettree()
    webbytitle = str(tree.xpath('//*[@id="HeaderUpcoming"]/div/div[1]/h2/a/text()'))
    for r in (("u'", ""), ("['", ""), ("[", ""), ("']", ""), ("\\n", ""), ("\\t", "")):
        webbytitle = webbytitle.replace(*r)
    webbytitle = unicode_string_cleanup(webbytitle)
    return webbytitle

def getwebbytime():
    now = datetime.datetime.utcnow()
    tree = gettree()
    webbytime = str(tree.xpath('//*[@id="HeaderUpcoming"]/div/div[1]/cite/span[1]/text()'))
    for r in (("['", ""), ("']", ""), ("\\n", ""), ("\\t", ""), ("@ ", ""), (" EST", ""), (",", ""), (".", "")):
        webbytime = webbytime.replace(*r)
    webbytime = parser.parse(str(webbytime))
    #webbytime = strptime(webbytime, '%b %d %Y %I:%M%p')
    return webbytime


def getwebbylink():
    tree = gettree()
    webbylink = str(tree.xpath('//*[@id="primary"]/div/ul/li[1]/div[2]/h1/a/@href'))
    for r in (("['", ""), ("']", "")):
        webbylink = webbylink.replace(*r)
    webbylink = str(webbylink.split("&", 1)[0])
    return webbylink

def getwebbybonus():
    tree = gettree()
    try:
        webbybonus = str(tree.xpath('//*[@id="primary"]/div/ul/li[1]/div[2]/div[2]/p/text()'))
        webbybonus = str(webbybonus.split("BONUS: ", 1)[1])
        for r in (("\\r", ""), ("\\n", ""), ("']",""), ("]",""), ('"',''), (" '","")):
            webbybonus = webbybonus.replace(*r)
        webbybonus = unicode_string_cleanup(webbybonus)
    except IndexError:
        webbybonus = ''
    return webbybonus

def getwebbytimeuntil():
    nowtime = datetime.datetime.utcnow()
    webbytime = getwebbytime()
    timecompare = get_timeuntil(nowtime, webbytime)
    return timecompare

def gettree():
    page = requests.get(url,headers = None)
    tree= html.fromstring(page.content)
    return tree
