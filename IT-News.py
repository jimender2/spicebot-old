import sopel.module
import requests
from xml.dom import minidom
from fake_useragent import UserAgent
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

## If Following Template
feedname = "iT News"
url = 'https://www.itnews.com.au/RSS/rss.ashx'
alt_url = 'https://www.itnews.com.au'
childnumber = 1
## End Of Template

## Based On Template
messagestring = str("[" + feedname + "] ")
trimmedname = feedname.replace(" ","").lower()
maincommand = str(trimmedname)
resetcommand = str(maincommand + 'reset')
lastbuilddatabase = str(maincommand + '_lastbuildcurrent')

## user agent and header
ua = UserAgent()
header = {'User-Agent': str(ua.chrome)}

@sopel.module.rate(120)
@sopel.module.commands(maincommand)
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    runprocess(bot)

@sopel.module.require_admin
@sopel.module.commands(resetcommand)
def reset(bot,trigger):
    for channel in bot.channels:
    	bot.say('Resetting LastBuildTime...')
    	bot.db.set_nick_value(channel, lastbuilddatabase, '')

## Automatic Run
@sopel.module.interval(60)
def autocheck(bot):
    for channel in bot.channels:
        page = requests.get(url, headers=header)
        if page.status_code == 200:
	    try:
                title, link = checkfornew(bot, page)
	    except TypeError:
		return
	    if title and link:
                bot.msg(channel, messagestring + title + ': ' + link)

def runprocess(bot):
    page = requests.get(url, headers=header)
    try:
        title, link = checkfornew(bot, page)
    except TypeError:
        title = feedname
        link = alt_url
    bot.say(messagestring + title + ': ' + link)  
		   
def checkLastBuildDate(bot, xmldoc):
    lastBuildXML = xmldoc.getElementsByTagName('pubDate')
    lastBuildXML = lastBuildXML[0].childNodes[0].nodeValue
    lastBuildXML = str(lastBuildXML)
    lastbuildcurrent = get_lastbuildcurrent(bot, lastBuildXML)
    if lastbuildcurrent:
	if lastBuildXML.strip() == lastbuildcurrent.strip():
	    newcontent = False
        else:
            newcontent = True
    else:
        newcontent = True
    set_lastbuildcurrent(bot, lastBuildXML)
    return newcontent

def checkfornew(bot, page):
    xml = page.text
    xml = xml.encode('ascii', 'ignore').decode('ascii')
    xmldoc = minidom.parseString(xml)
    newcontent = checkLastBuildDate(bot, xmldoc)
    if newcontent == True:
	titles = xmldoc.getElementsByTagName('title')
        title = titles[childnumber].childNodes[0].nodeValue
        links = xmldoc.getElementsByTagName('link')
        link = links[childnumber].childNodes[0].nodeValue.split("?")[0]
        return title, link

def get_lastbuildcurrent(bot, lastBuildXML):
    for channel in bot.channels:
        lastbuildcurrent = bot.db.get_nick_value(channel, lastbuilddatabase) or 0
    return lastbuildcurrent

def set_lastbuildcurrent(bot, lastbuildcurrent):
    for channel in bot.channels:
        bot.db.set_nick_value(channel, lastbuilddatabase, lastbuildcurrent)
