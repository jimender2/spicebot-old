#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import ConfigParser
import requests
from lxml import html
import datetime
from time import strptime
from dateutil import parser
import calendar
import arrow
import pytz
from dateutil import tz
from xml.dom import minidom
from fake_useragent import UserAgent
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


# user agent and header
ua = UserAgent()
header = {'User-Agent': str(ua.chrome)}

# author deathbybandaid

feeds_dir = "feeds/"
feeds_file_path = os.path.join(moduledir, feeds_dir)


# Automatic Run
@sopel.module.interval(60)
def autofeeds(bot):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'feeds')
    if not enablestatus:
        # feeds dynamic Class
        feeds = class_create('feeds')
        feeds = feeds_configs(bot, feeds)
        feed_enabled = get_database_value(bot, channelselect, 'feeds_enabled') or []
        for feed in feeds.list:
            if feed in feed_enabled:
                dispmsg = feeds_display(bot, botcom, feed, feeds, 1) or []
                if dispmsg != []:
                    osd(bot, botcom.channel_current, 'say', dispmsg)


@sopel.module.commands('feeds', 'packt', 'spicewebby', 'atwebby', 'comptiawebby', 'spiceworkswebby', 'actualtechwebby')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'feeds')
    if not enablestatus:
        if trigger.group(1) == 'feeds':
            execute_main(bot, trigger, triggerargsarray, botcom, instigator)
        else:
            # feeds dynamic Class
            feeds = class_create('feeds')
            feeds = feeds_configs(bot, feeds)
            feed = trigger.group(1)
            if feed == 'spicewebby':
                feed = 'spiceworkswebby'
            elif feed == 'atwebby':
                feed = 'actualtechwebby'
            dispmsg = feeds_display(bot, botcom, feed, feeds, 1) or []
            if dispmsg == []:
                osd(bot, botcom.channel_current, 'say', feed_select + " appears to have had an unknown error.")
            else:
                osd(bot, botcom.channel_current, 'say', dispmsg)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):

    # feeds dynamic Class
    feeds = class_create('feeds')

    valid_commands = ['enable', 'disable', 'reset', 'run']
    command = get_trigger_arg(bot, [x for x in triggerargsarray if x in valid_commands], 1) or 'run'
    if command in triggerargsarray:
        triggerargsarray.remove(command)

    feeds = feeds_configs(bot, feeds)

    feed_select = get_trigger_arg(bot, [x for x in triggerargsarray if x in feeds.list or x == 'all'], 1) or 'nofeed'
    if feed_select == 'nofeed':
        feed_list = get_trigger_arg(bot, feeds.list, 'list')
        osd(bot, botcom.channel_current, 'say', "Valid Feeds are " + feed_list)
        return

    channelselect = get_trigger_arg(bot, [x for x in triggerargsarray if x in feeds.list], 1) or botcom.channel_current

    feed_enabled = get_database_value(bot, channelselect, 'feeds_enabled') or []

    if command == 'reset':
        bot.say("reset")
        return

    elif command == 'enable':
        if feed_select in feed_enabled:
            osd(bot, botcom.channel_current, 'say', feed_select + " seems to already be " + command + "d.")
            return
        adjust_database_array(bot, channelselect, [feed_select], 'feeds_enabled', 'add')
        osd(bot, botcom.channel_current, 'say', feed_select + " has been " + command + "d.")
        return

    elif command == 'disable':
        if feed_select not in feed_enabled:
            osd(bot, botcom.channel_current, 'say', feed_select + " seems to already be " + command + "d.")
            return
        adjust_database_array(bot, channelselect, [feed_select], 'feeds_enabled', 'del')
        osd(bot, botcom.channel_current, 'say', feed_select + " has been " + command + "d.")
        return

    elif command == 'run':
        if feed_select == 'all':
            current_feed_list = feeds.list
        else:
            current_feed_list = [feed_select]
        for feed in current_feed_list:
            dispmsg = feeds_display(bot, botcom, feed, feeds, 1) or []
            if dispmsg == []:
                osd(bot, botcom.channel_current, 'say', feed_select + " appears to have had an unknown error.")
            else:
                osd(bot, botcom.channel_current, 'say', dispmsg)
        return


def feeds_display(bot, botcom, feed, feeds, displayifnotnew):

    dispmsg = []
    titleappend = 0

    url = eval("feeds." + feed + ".url")
    page = requests.get(url, headers=header)
    tree = html.fromstring(page.content)
    if page.status_code == 200:

        now = datetime.datetime.utcnow()
        now = now.replace(tzinfo=pytz.UTC)

        displayname = eval("feeds." + feed + ".displayname")

        feed_type = eval("feeds." + feed + ".type")

        if feed_type == 'rss':

            parentnumber = int(eval("feeds." + feed + ".parentnumber"))
            childnumber = int(eval("feeds." + feed + ".childnumber"))

            lastbuildcurrent = get_database_value(bot, bot.nick, feed + '_lastbuildcurrent') or 0

            xml = page.text
            xml = xml.encode('ascii', 'ignore').decode('ascii')
            xmldoc = minidom.parseString(xml)

            lastBuildXML = xmldoc.getElementsByTagName('pubDate')
            lastBuildXML = lastBuildXML[0].childNodes[0].nodeValue
            lastBuildXML = str(lastBuildXML)

            newcontent = True
            if lastBuildXML.strip() == lastbuildcurrent:
                newcontent = False

            if displayifnotnew or newcontent:

                titleappend = 1

                titles = xmldoc.getElementsByTagName('title')
                title = titles[parentnumber].childNodes[0].nodeValue
                dispmsg.append(title)

                links = xmldoc.getElementsByTagName('link')
                link = links[childnumber].childNodes[0].nodeValue.split("?")[0]
                dispmsg.append(link)

                lastbuildcurrent = lastBuildXML.strip()
                set_database_value(bot, bot.nick, feed + '_lastbuildcurrent', lastbuildcurrent)

        elif feed_type == 'webinar':

            scrapetime = eval("feeds." + feed + ".time")
            scrapetimezone = eval("feeds." + feed + ".timezone")

            webbytime = str(tree.xpath(scrapetime))
            for r in (("['", ""), ("']", ""), ("\\n", ""), ("\\t", ""), ("@ ", "")):
                webbytime = webbytime.replace(*r)

            if feed == 'spiceworkswebby':
                webbytime = str(webbytime.split("+", 1)[0])

            webbytz = pytz.timezone(scrapetimezone)
            webbytime = parser.parse(webbytime)
            webbytime = webbytz.localize(webbytime)

            timeuntil = (webbytime - now).total_seconds()

            if displayifnotnew or (int(timeuntil) < 900 and int(timeuntil) > 840):

                titleappend = 1

                timecompare = get_timeuntil(now, webbytime)
                dispmsg.append("{" + timecompare + "}")

                scrapetitle = eval("feeds." + feed + ".title")
                webbytitle = str(tree.xpath(scrapetitle))
                for r in (("u'", ""), ("['", ""), ("[", ""), ("']", ""), ("\\n", ""), ("\\t", "")):
                    webbytitle = webbytitle.replace(*r)
                webbytitle = unicode_string_cleanup(webbytitle)
                dispmsg.append(webbytitle)

                scrapelink = eval("feeds." + feed + ".link")
                webbylink = str(tree.xpath(scrapelink))
                for r in (("['", ""), ("']", "")):
                    webbylink = webbylink.replace(*r)
                if feed == 'actualtechwebby':
                    webbylink = str(url + webbylink.split("&", 1)[0])
                webbylinkprecede = eval("feeds." + feed + ".linkprecede")
                if webbylinkprecede != 'noprecede':
                    webbylink = str(webbylinkprecede + webbylink)
                dispmsg.append(webbylink)

                scrapebonus = eval("feeds." + feed + ".bonus")
                if scrapebonus != 'nobonus':
                    webbybonus = ''
                    try:
                        webbybonus = str(tree.xpath(scrapebonus))
                        if feed == 'spiceworkswebby':
                            webbybonus = str(webbybonus.split("BONUS: ", 1)[1])
                        for r in (("\\r", ""), ("\\n", ""), ("']", ""), ("]", ""), ('"', ''), (" '", ""), ("['", ""), ("[", "")):
                            webbybonus = webbybonus.replace(*r)
                        webbybonus = unicode_string_cleanup(webbybonus)
                    except IndexError:
                        webbybonus = ''
                    if webbybonus != '':
                        dispmsg.append('BONUS: ' + webbybonus)

        elif feed_type == 'daily':

            timehour = eval("feeds." + feed + ".hour")
            timeminute = eval("feeds." + feed + ".minute")
            scrapetimezone = eval("feeds." + feed + ".timezone")

            scrapetitle = eval("feeds." + feed + ".title")
            title = str(tree.xpath(scrapetitle))
            for r in (("\\t", ""), ("\\n", ""), ("['", ""), ("']", ""), ("]", "")):
                title = title.replace(*r)
            if title == "[]" or title == '':
                title = "No Book Today"
            dispmsg.append(title)

            dailytz = pytz.timezone(scrapetimezone)
            nowtime = datetime.datetime.now(dailytz)
            tomorrow = nowtime + datetime.timedelta(days=1)
            dailytime = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, int(timehour), int(timeminute), 0, 0)
            dailytime = dailytz.localize(dailytime)
            timeuntil = (dailytime - nowtime).total_seconds()

            if displayifnotnew or int(timeuntil) < 60:

                titleappend = 1

                timecompare = get_timeuntil(now, dailytime)
                dispmsg.append("{Next " + timecompare + "}")

                dispmsg.append("URL: " + url)

        if titleappend:
            dispmsg.insert(0, "[" + displayname + "]")

    return dispmsg


# rss feeds list
def feeds_configs(bot, feeds):
    feeds.list = []
    for feed_dir_type in os.listdir(feeds_file_path):
        feed_type_file_path = os.path.join(feeds_file_path, feed_dir_type)
        for feed in os.listdir(feed_type_file_path):

            # Add to main list
            feeds.list.append(feed)

            # Every feed gets a class
            current_feed = class_create(feed)
            exec("feeds." + feed + " = current_feed")

            # file name
            exec("feeds." + feed + ".feed_filename = feed")

            # get file path
            feedfile = os.path.join(feed_type_file_path, feed)
            exec("feeds." + feed + ".file_path = feedfile")

            # Read configuration
            config = ConfigParser.ConfigParser()
            config.read(feedfile)
            for each_section in config.sections():
                for (each_key, each_val) in config.items(each_section):
                    exec("feeds." + feed + "." + each_key + " = each_val")

    return feeds
