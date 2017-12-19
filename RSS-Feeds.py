import sopel.module
import requests
from xml.dom import minidom
from fake_useragent import UserAgent
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

feednamearray = ['Spiceworks Contests']
urlarray = ['https://community.spiceworks.com/feed/forum/1550.rss']
childarray = [2]

@sopel.module.require_admin
@sopel.module.commands(resetcommand)
def reset(bot,trigger):
    for feedname,url,childnumber in zip(feednamearray,urlarray,childarray):
        lastbuilddatabase = str(feedname + '_lastbuildcurrent')
        for channel in bot.channels:
    	    bot.say('Resetting LastBuildTime for ' + str(feedname))
    	    bot.db.set_nick_value(channel, lastbuilddatabase, '')

## Automatic Run
@sopel.module.interval(60)
def autorss(bot):
    for feedname,url,childnumber in zip(feednamearray,urlarray,childarray):
        lastbuilddatabase = str(feedname + '_lastbuildcurrent')
        for channel in bot.channels:
            page = requests.get(url, headers=header)
            if page.status_code == 200:
	            try:
                    title, link = checkfornew(bot, page, childnumber, lastbuilddatabase)
    	        except TypeError:
	    	        return
	            if title and link:
                    bot.msg(channel, messagestring + title + ': ' + link)
                
def checkfornew(bot, page, childnumber, lastbuilddatabase):
    xml = page.text
    xml = xml.encode('ascii', 'ignore').decode('ascii')
    xmldoc = minidom.parseString(xml)
    newcontent = checkLastBuildDate(bot, xmldoc, lastbuilddatabase)
    if newcontent == True:
	    titles = xmldoc.getElementsByTagName('title')
        title = titles[childnumber].childNodes[0].nodeValue
        links = xmldoc.getElementsByTagName('link')
        link = links[childnumber].childNodes[0].nodeValue.split("?")[0]
        return title, link

def checkLastBuildDate(bot, xmldoc, lastbuilddatabase):
    lastBuildXML = xmldoc.getElementsByTagName('pubDate')
    lastBuildXML = lastBuildXML[0].childNodes[0].nodeValue
    lastBuildXML = str(lastBuildXML)
    lastbuildcurrent = get_lastbuildcurrent(bot, lastBuildXML, lastbuilddatabase)
    if lastbuildcurrent:
	if lastBuildXML.strip() == lastbuildcurrent.strip():
	    newcontent = False
        else:
            newcontent = True
    else:
        newcontent = True
    set_lastbuildcurrent(bot, lastBuildXML)
    return newcontent

def get_lastbuildcurrent(bot, lastBuildXML, lastbuilddatabase):
    for channel in bot.channels:
        lastbuildcurrent = bot.db.get_nick_value(channel, lastbuilddatabase) or 0
    return lastbuildcurrent
