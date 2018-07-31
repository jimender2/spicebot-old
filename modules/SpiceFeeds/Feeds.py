#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import ConfigParser
import requests
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


@sopel.module.commands('feeds')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


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

    feed_url = eval("feeds." + feed + ".url")
    page = requests.get(feed_url, headers=header)
    if page.status_code == 200:

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

            if newcontent or displayifnotnew:

                titles = xmldoc.getElementsByTagName('title')
                title = titles[parentnumber].childNodes[0].nodeValue
                dispmsg.append(title)

                links = xmldoc.getElementsByTagName('link')
                link = links[childnumber].childNodes[0].nodeValue.split("?")[0]
                dispmsg.append(link)

                lastbuildcurrent = lastBuildXML.strip()
                set_database_value(bot, bot.nick, feed + '_lastbuildcurrent', lastbuildcurrent)

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
