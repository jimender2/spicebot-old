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
sys.path.append(moduledir)
from SpicebotShared import *

url = 'https://community.spiceworks.com/calendar'

@sopel.module.commands('spicewebby')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    page = requests.get(url,headers = None)
    if page.status_code == 200:
        now = datetime.datetime.utcnow()
        webbytimeuntil = getwebbytimeuntil()
        webbybonus = getwebbybonus()
        webbytitle = getwebbytitle()
        webbylink = getwebbylink()
        bot.say(webbytimeuntil + '     Title: ' + webbytitle + '     Link: ' + webbylink)
        if webbybonus != '[]' and webbybonus != '' and webbybonus != ' ':
            bot.say('BONUS: ' + webbybonus)

@sopel.module.interval(60)
def webbyauto(bot):
    page = requests.get(url,headers = None)
    if page.status_code == 200:
        for channel in bot.channels:
            now = datetime.datetime.utcnow()
            webbytime = getwebbytime()
            if str(now.month) == str(webbytime.month) and str(now.day) == str(webbytime.day):
                if str(now.hour) == str(int(webbytime.hour) - 1) and str(now.minute) == '45':
                    webbybonus = getwebbybonus()
                    webbytitle = getwebbytitle()
                    webbylink = getwebbylink()
                    bot.msg(channel, '[15 Minute Webby Reminder]     Title: ' + str(webbytitle) + '     Link: ' + str(webbylink))
                    if webbybonus != '[]' and webbybonus != '' and webbybonus != ' ':
                        bot.msg(channel, str(webbybonus))

def getwebbytime():
    now = datetime.datetime.utcnow()
    tree = gettree()
    webbytime = str(tree.xpath('//*[@id="primary"]/div/ul/li[1]/div[1]/div[2]/span[@title]/@datetime'))
    for r in (("['", ""), ("']", "")):
        webbytime = webbytime.replace(*r)
    webbytime = str(webbytime.split("+", 1)[0])
    webbytime = parser.parse(webbytime)
    return webbytime

def getwebbytitle():
    tree = gettree()
    webbytitle = str(tree.xpath('//*[@id="primary"]/div/ul/li[1]/div[2]/h1/a/text()'))
    for r in (("\u2013", "-"), ("\u2019", "'"), ("\u2026", "..."), ("\u2019", "'"), ("u'", ""), ("['", ""), ("[", ""), ("']", "")):
        webbytitle = webbytitle.replace(*r)
    return webbytitle

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
        for r in (("\u2013", "-"), ("\\r", ""), ("\\n", ""), ("']",""), ("]",""), ('"',''), (" '","")):
            webbybonus = webbybonus.replace(*r)
    except IndexError:
        webbybonus = ''
    return webbybonus

def getwebbytimeuntil():
    now = datetime.datetime.utcnow()
    webbytime = getwebbytime()
    a = arrow.get(now)
    b = arrow.get(webbytime)
    timecompare = (b.humanize(a, granularity='auto'))
    webbytimeuntil = str(timecompare)
    return webbytimeuntil

def gettree():
    page = requests.get(url,headers = None)
    tree= html.fromstring(page.content)
    return tree
