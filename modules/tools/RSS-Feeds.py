#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import requests
from xml.dom import minidom
from fake_useragent import UserAgent
import sys
import os

## user agent and header
ua = UserAgent()
header = {'User-Agent': str(ua.chrome)}

@sopel.module.require_admin
@sopel.module.commands('rssreset')
def reset(bot,trigger):
    for feedname,url,childnumber,parent in zip(feednamearray,urlarray,childarray,parentarray):
	trimmedname = feedname.replace(" ","").lower()
	maincommand = str(trimmedname)
        lastbuilddatabase = str(maincommand + '_lastbuildcurrent')
        for channel in bot.channels:
    	    bot.say('Resetting LastBuildTime for ' + str(feedname))
    	    bot.db.set_nick_value(channel, lastbuilddatabase, '')

## Automatic Run
@sopel.module.interval(60)
def autorss(bot):
    for feedname,url,childnumber,parent in zip(feednamearray,urlarray,childarray,parentarray):
        trimmedname = feedname.replace(" ","").lower()
	maincommand = str(trimmedname)
        lastbuilddatabase = str(maincommand + '_lastbuildcurrent')
	messagestring = str("[" + feedname + "] ")
        for channel in bot.channels:
            page = requests.get(url, headers=header)
            if page.status_code == 200:
                try:
                    title, link = checkfornew(bot, page, childnumber, lastbuilddatabase, parent)
                except TypeError:
                    return
                if title and link:
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
