#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import requests
from lxml import html
from fake_useragent import UserAgent
from datetime import datetime, timedelta
import datetime
import arrow
import time
import sys
import os
from datetime import datetime
from pytz import timezone
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

# new book is Midnight GMT/BST
tz = timezone('Europe/London')
packthour = str(0)
packtminute = str(10)

@sopel.module.commands('packt')
def execute_main(bot, trigger):
    packttimediff = getpackttimediff()
    if trigger.group(2):
        if trigger.group(2) == 'time':
            bot.say(str(packttimediff))
        else:
            normalrun='true'
    else:
        normalrun='true'
    try:
        if normalrun:
            title = getPacktTitle()
            bot.say("Packt Free Book Today is: " + title + str(packttimediff) + '     URL: https://www.packtpub.com/packt/offers/free-learning')
    except UnboundLocalError:
        return
    
@sopel.module.interval(60)
def getpackt(bot):
    now = datetime.now(tz)
    if now.hour == int(packthour) and now.minute == int(packtminute):
        title = getPacktTitle()
        packttimediff = getpackttimediff()
        for channel in bot.channels:
            bot.msg(channel, "Packt Free Book Today is: " + title +  str(packttimediff) + '     URL: https://www.packtpub.com/packt/offers/free-learning')

def getPacktTitle():
        url = 'https://www.packtpub.com/packt/offers/free-learning'

        ua = UserAgent()
        header = {'User-Agent':str(ua.chrome)}
        page = requests.get(url,headers = header)

        if page.status_code == 200:
                tree = html.fromstring(page.content)
                title = str(tree.xpath('//*[@id="deal-of-the-day"]/div/div/div[2]/div[2]/h2/text()'))
                title = title.replace("\\t","")
                title = title.replace("\\n","")
                return title
        else:
                title = 'Could not get Title. The status code was : ' + page.status_code
        return title

def getpackttimediff():
    nowtime = datetime.datetime.now(tz)
    tomorrow = nowtime + timedelta(days=1)
    packtnext = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, int(packthour), int(packtminute), 0, 0)
    timecompare = get_timeuntil(nowtime, packtnext)
    packttimediff = str('     Next Book: ' + timecompare)
    return packttimediff
