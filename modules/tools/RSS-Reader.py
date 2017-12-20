#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import requests
from xml.dom import minidom
from fake_useragent import UserAgent
import sys
import os
import ConfigParser

RSSFEEDSDIR = "/home/sopel/.sopel/spicebot/RSS-Feeds/"

## user agent and header
ua = UserAgent()
header = {'User-Agent': str(ua.chrome)}

@sopel.module.require_admin
@sopel.module.commands('rssreset')
def reset(bot,trigger):
    feedselect = trigger.group(2)
    for c in bot.channels:
        channel = c
    if not feedselect:
        bot.say("Which Feed are we resetting?")
    elif feedselect == 'all':
        for filename in os.listdir(RSSFEEDSDIR):
            configfile = os.path.join(RSSFEEDSDIR, filename)
            config = ConfigParser.ConfigParser()
            config.read(configfile)
            feedname = config.get("configuration","feedname")
            trimmedname = feedname.replace(" ","").lower()
            lastbuilddatabase = str(trimmedname + '_lastbuildcurrent')
            bot.say('Resetting LastBuildTime for ' + str(feedname))
            bot.db.set_nick_value(channel, lastbuilddatabase, None)
    else:
        lastbuilddatabase = str(feedselect + '_lastbuildcurrent')
        istherafeed = bot.db.get_nick_value(channel, lastbuilddatabase) or 0
        if istherafeed:
            bot.say('Resetting LastBuildTime for ' + str(feedname))
            bot.db.set_nick_value(channel, lastbuilddatabase, None)
        else:
            bot.say("There doesn't appear to be record of that feed.")


## Automatic Run
@sopel.module.interval(30)
def autorss(bot):
    for c in bot.channels:
        channel = c
    rssarray = []
    for filename in os.listdir(RSSFEEDSDIR):
        rssarray.append(filename)
    for rssfeed in rssarray:
        configfile = os.path.join(RSSFEEDSDIR, rssfeed)
        config = ConfigParser.ConfigParser()
        config.read(configfile)
        feedname = config.get("configuration","feedname")
        url = str(config.get("configuration","url"))
        parentnumber = int(config.get("configuration","parentnumber"))
        childnumber = int(config.get("configuration","childnumber"))
        lastbuilddatabase = str(rssfeed + '_lastbuildcurrent')
        messagestring = str("[" + feedname + "] ")
        page = requests.get(url, headers=header)
        title, link = 'nope', 'nada'
        if page.status_code == 200:
            title, link = checkfornew(bot, page, childnumber, lastbuilddatabase, parentnumber)
        bot.msg(channel, messagestring + title + ': ' + link)
                
def checkfornew(bot, page, childnumber, lastbuilddatabase, parent):
    xml = page.text
    xml = xml.encode('ascii', 'ignore').decode('ascii')
    xmldoc = minidom.parseString(xml)
    newcontent = checkLastBuildDate(bot, xmldoc, lastbuilddatabase)
    if newcontent == True:
        titles = xmldoc.getElementsByTagName('title')
        title = titles[parent].childNodes[0].nodeValue
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
    set_lastbuildcurrent(bot, lastBuildXML, lastbuilddatabase)
    return newcontent

def get_lastbuildcurrent(bot, lastBuildXML, lastbuilddatabase):
    for channel in bot.channels:
        lastbuildcurrent = bot.db.get_nick_value(channel, lastbuilddatabase) or 0
    return lastbuildcurrent

def set_lastbuildcurrent(bot, lastbuildcurrent, lastbuilddatabase):
    for channel in bot.channels:
        bot.db.set_nick_value(channel, lastbuilddatabase, lastbuildcurrent)
