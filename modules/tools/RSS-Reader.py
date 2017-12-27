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
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

## user agent and header
ua = UserAgent()
header = {'User-Agent': str(ua.chrome)}

@sopel.module.require_admin
@sopel.module.commands('rssreset')
def reset(bot,trigger):
    feedselect = trigger.group(2)
    RSSFEEDSDIR = str("/home/sopel/.sopel/"+bot.nick.lower()+"/RSS-Feeds/")
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
            bot.db.set_nick_value(bot.nick, lastbuilddatabase, None)
    else:
        lastbuilddatabase = str(feedselect + '_lastbuildcurrent')
        istherafeed = bot.db.get_nick_value(bot.nick, lastbuilddatabase) or 0
        if istherafeed:
            bot.say('Resetting LastBuildTime for ' + str(feedselect))
            bot.db.set_nick_value(bot.nick, lastbuilddatabase, None)
        else:
            bot.say("There doesn't appear to be record of that feed.")


## Automatic Run
@sopel.module.interval(60)
def autorss(bot):
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
        pubdatetype = str(config.get("configuration","pubdatetype"))
        linktype = str(config.get("configuration","linktype"))
        lastbuilddatabase = str(rssfeed + '_lastbuildcurrent')
        messagestring = str("[" + feedname + "] ")
        page = requests.get(url, headers=header)
        if page.status_code == 200:
            xml = page.text
            xml = xml.encode('ascii', 'ignore').decode('ascii')
            xmldoc = minidom.parseString(xml)
            lastBuildXML = xmldoc.getElementsByTagName(pubdatetype)
            lastBuildXML = lastBuildXML[0].childNodes[0].nodeValue
            lastBuildXML = str(lastBuildXML)
            lastbuildcurrent = bot.db.get_nick_value(bot.nick, lastbuilddatabase) or 0
            newcontent = True
            if lastBuildXML.strip() == lastbuildcurrent:
                newcontent = False
            if newcontent == True:
                titles = xmldoc.getElementsByTagName('title')
                title = titles[parentnumber].childNodes[0].nodeValue
                links = xmldoc.getElementsByTagName(linktype)
                link = links[childnumber].childNodes[0].nodeValue.split("?")[0]
                lastbuildcurrent = lastBuildXML.strip()
                bot.db.set_nick_value(bot.nick, lastbuilddatabase, lastbuildcurrent)
                for channel in bot.channels:
                    bot.msg(channel, messagestring + title + ': ' + link)
