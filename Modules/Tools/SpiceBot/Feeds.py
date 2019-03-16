#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel.module

# imports for system and OS access, directories
import os
import sys

# imports based on THIS file
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# Ensure Encoding
reload(sys)
sys.setdefaultencoding('utf-8')


# @event('001')
# @rule('.*')
# @sopel.module.thread(True)
# def auto_feeds(bot, trigger):
#
#    # don't run jobs if not ready
#    while not bot_startup_requirements_met(bot, ["monologue"]):
#        pass
#
#    if "feeds" not in bot.memory:
#        feed_configs(bot)
#
#    bot_startup_requirements_set(bot, "feeds")
#
#    for feed in bot.memory["feeds"].keys():
#        feeds_grab(bot, feed)
#        # Thread(target=feeds_thread, args=(bot, feed,)).start()


@sopel.module.interval(57)
@sopel.module.thread(True)
def auto_feeds(bot, trigger):

    # don't run jobs if not ready
    while not bot_startup_requirements_met(bot, ["monologue"]):
        pass

    if "feeds" not in bot.memory:
        feed_configs(bot)

    bot_startup_requirements_set(bot, "feeds")

    for feed in bot.memory["feeds"].keys():
        feeds_grab(bot, feed)


def feeds_thread(bot, feed):
    while True:
        time.sleep(57)
        dispmsg = bot_dictcom_feeds_handler(bot, feed, False)
        if dispmsg != []:

            for channel in bot.privileges.keys():
                feeds_enabled = get_channel_value(bot, channel, "long", "feeds", "enabled") or []
                if feed in feeds_enabled:
                    osd(bot, str(channel), 'say', dispmsg)

            for user in bot.memory["botdict"]["tempvals"]["servers_list"][str(bot.memory["botdict"]["tempvals"]['server'])]['all_current_users']:
                feed_enabled = get_nick_value(bot, user, "long", "feeds", "enabled") or []
                if feed in feed_enabled:
                    osd(bot, user, 'priv', dispmsg)


def feeds_grab(bot, feed):
    dispmsg = bot_dictcom_feeds_handler(bot, feed, False)
    if dispmsg != []:

        for channel in bot.privileges.keys():
            feeds_enabled = get_channel_value(bot, channel, "long", "feeds", "enabled") or []
            if feed in feeds_enabled:
                osd(bot, str(channel), 'say', dispmsg)

        for user in bot.memory["botdict"]["tempvals"]["servers_list"][str(bot.memory["botdict"]["tempvals"]['server'])]['all_current_users']:
            feed_enabled = get_nick_value(bot, user, "long", "feeds", "enabled") or []
            if feed in feed_enabled:
                osd(bot, user, 'priv', dispmsg)


@sopel.module.commands('feed', "feeds")
@sopel.module.thread(True)
def mainfunction(bot, trigger):

    botcom = bot_module_prerun(bot, trigger)
    if not botcom.modulerun:
        return

    if not botcom.multiruns:
        execute_main(bot, trigger, botcom)
    else:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, botcom.triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            botcom.triggerargsarray = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, botcom)

    botdict_save(bot)


def execute_main(bot, trigger, botcom):

    if "feeds" not in bot.memory:
        feed_configs(bot)

    if not len(bot.memory['feeds'].keys()):
        return osd(bot, botcom.channel_current, 'say', "There are no valid feeds!!")

    valid_commands = ['enable', 'disable', 'reset', 'run', 'subscribe', 'unsubscribe']
    command = spicemanip(bot, [x for x in botcom.triggerargsarray if x in valid_commands], 1) or 'run'
    if command in botcom.triggerargsarray:
        botcom.triggerargsarray.remove(command)

    feed_select = spicemanip(bot, [x for x in botcom.triggerargsarray if x in bot.memory['feeds'].keys() or x == 'all'], 1) or None
    if not feed_select:
        feed_list = spicemanip(bot, bot.memory['feeds'].keys(), 'list')
        osd(bot, botcom.channel_current, 'say', "Valid Feeds are " + feed_list)
        return

    if feed_select == 'all':
        current_feed_list = bot.memory['feeds'].keys()
    else:
        current_feed_list = []
        for word in botcom.triggerargsarray:
            if word in bot.memory['feeds'].keys():
                current_feed_list.append(word)

    if command == 'run':
        for feed in current_feed_list:
            dispmsg = bot_dictcom_feeds_handler(bot, feed, True)
            if dispmsg == []:
                osd(bot, botcom.channel_current, 'say', feed_select + " appears to have had an unknown error.")
            else:
                if feed_select == 'all':
                    osd(bot, botcom.instigator, 'priv', dispmsg)
                else:
                    osd(bot, botcom.channel_current, 'say', dispmsg)
        return

    if command == 'subscribe':
        instigatormodulesarray = get_nick_value(bot, botcom.instigator, "long", "feeds", "enabled") or []
        newlist = []
        for feed in current_feed_list:
            if feed not in instigatormodulesarray:
                newlist.append(feed)
        if newlist != []:
            adjust_nick_array(bot, botcom.instigator, "long", "feeds", "enabled", newlist, "add")
            osd(bot, botcom.channel_current, 'say', "You are now " + command + "d to " + spicemanip(bot, newlist, 'list'))
        else:
            osd(bot, botcom.channel_current, 'say', "No selected feeds to " + command + ".")
        return

    if command == 'unsubscribe':
        instigatormodulesarray = get_nick_value(bot, botcom.instigator, "long", "feeds", "enabled") or []
        newlist = []
        for feed in current_feed_list:
            if feed in instigatormodulesarray:
                newlist.append(feed)
        if newlist != []:
            adjust_nick_array(bot, botcom.instigator, "long", "feeds", "enabled", newlist, "del")
            osd(bot, botcom.channel_current, 'say', "You are now " + command + "d from " + spicemanip(bot, newlist, 'list'))
        else:
            osd(bot, botcom.channel_current, 'say', "No selected feeds to " + command + ".")
        return

    if not bot_command_run_check(bot, botcom, ['admin', 'owner', 'OWNER', 'OP', 'ADMIN']):
        osd(bot, botcom.channel_current, 'say', "Only Bot Admins and Channel Operators are able to adjust Feed settings.")
        return

    if command == 'reset':
        newlist = []
        for feed in current_feed_list:
            feed_type = bot.memory['feeds'][feed]["type"]
            if feed_type in ['rss', 'youtube', 'github', 'redditrss', 'redditapi', 'twitter']:
                newlist.append(feed)
        if newlist != []:
            for feed in newlist:
                reset_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildtime')
                reset_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildtitle')
                reset_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildlink')
            osd(bot, botcom.channel_current, 'say', spicemanip(bot, newlist, 'list') + " " + hashave(newlist) + " been " + command + ".")
        else:
            osd(bot, botcom.channel_current, 'say', "No selected feeds to " + command + ".")
        return

    channelselect = spicemanip(bot, [x for x in botcom.triggerargsarray if x in bot.privileges.keys()], 1) or botcom.channel_current

    if command == 'enable':
        feeds_enabled = get_channel_value(bot, channelselect, "long", "feeds", "enabled") or []
        newlist = []
        for feed in current_feed_list:
            if feed not in feeds_enabled:
                newlist.append(feed)
        if newlist != []:
            adjust_channel_array(bot, channelselect, "long", "feeds", "enabled", newlist, "add")
            osd(bot, botcom.channel_current, 'say', spicemanip(bot, newlist, 'list') + " " + hashave(newlist) + " been " + command + "d for " + str(channelselect) + ".")
        else:
            osd(bot, botcom.channel_current, 'say', "No selected feeds to " + command + ".")
        return

    if command == 'disable':
        feeds_enabled = get_channel_value(bot, channelselect, "long", "feeds", "enabled") or []
        newlist = []
        for feed in current_feed_list:
            if feed in feeds_enabled:
                newlist.append(feed)
        if newlist != []:
            adjust_channel_array(bot, channelselect, "long", "feeds", "enabled", newlist, "del")
            osd(bot, botcom.channel_current, 'say', spicemanip(bot, newlist, 'list') + " " + hashave(newlist) + " been " + command + "d for " + str(channelselect) + ".")
        else:
            osd(bot, botcom.channel_current, 'say', "No selected feeds to " + command + ".")
        return


def feed_configs(bot):

    bot.memory['feeds'] = dict()

    dirdict = {
                "name": "feeds",
                "dirname": "Feeds",
                }

    filedicts, filecount = configs_dir_read(bot, dirdict)

    for dict_from_file in filedicts:

        comconf = dict_from_file["filename"]

        if "type" not in dict_from_file.keys():
            dict_from_file["type"] = quick_coms_type

        if "displayname" not in dict_from_file.keys():
            dict_from_file["displayname"] = None

        if "url" not in dict_from_file.keys():
            dict_from_file["url"] = None

        if dict_from_file["type"] == "redditapi":

            if "path" not in dict_from_file.keys():
                dict_from_file["path"] = None

            if not dict_from_file["url"]:
                dict_from_file["url"] = "https://www.reddit.com"

        if dict_from_file["type"] == "twitter":

            if "handle" not in dict_from_file.keys():
                dict_from_file["handle"] = None

            if not dict_from_file["url"]:
                dict_from_file["url"] = "https://twitter.com"

        if dict_from_file["type"] == "googlecalendar":

            if "calendar" not in dict_from_file.keys():
                dict_from_file["calendar"] = None

            if "link" not in dict_from_file.keys():
                dict_from_file["link"] = None

            if not dict_from_file["url"]:
                dict_from_file["url"] = "https://google.com"

        if dict_from_file["type"] == "dailyscrapes":

            if "scrapetitle" not in dict_from_file.keys():
                dict_from_file["scrapetitle"] = None

            if "scrapehour" not in dict_from_file.keys():
                dict_from_file["scrapehour"] = 1

            if "scrapeminute" not in dict_from_file.keys():
                dict_from_file["scrapeminute"] = 1

            if "scrapetimezone" not in dict_from_file.keys():
                dict_from_file["scrapetimezone"] = "UTC"

            if "scrapelink" not in dict_from_file.keys():
                dict_from_file["scrapelink"] = None

            if "linkprecede" not in dict_from_file.keys():
                dict_from_file["linkprecede"] = None

        if dict_from_file["type"] == "events":

            if "scrapetitle" not in dict_from_file.keys():
                dict_from_file["scrapetitle"] = None

            if "eventmonth" not in dict_from_file.keys():
                dict_from_file["eventmonth"] = 1

            if "eventday" not in dict_from_file.keys():
                dict_from_file["eventday"] = 1

            if "eventhour" not in dict_from_file.keys():
                dict_from_file["eventhour"] = 0

            if "eventminute" not in dict_from_file.keys():
                dict_from_file["eventminute"] = 0

            if "timezone" not in dict_from_file.keys():
                dict_from_file["timezone"] = "UTC"

            if "rightnow" not in dict_from_file.keys():
                dict_from_file["rightnow"] = None

        if dict_from_file["type"] == "scrapes":

            if "scrapetitle" not in dict_from_file.keys():
                dict_from_file["scrapetitle"] = None

            if "scrapetime" not in dict_from_file.keys():
                dict_from_file["scrapetime"] = None

            if "scrapetimezone" not in dict_from_file.keys():
                dict_from_file["scrapetimezone"] = "UTC"

            if "scrapelink" not in dict_from_file.keys():
                dict_from_file["scrapelink"] = None

            if "linkprecede" not in dict_from_file.keys():
                dict_from_file["linkprecede"] = None

        if dict_from_file["type"] == "webinarscrapes":

            if "scrapetime" not in dict_from_file.keys():
                dict_from_file["scrapetime"] = None

            if "scrapetitle" not in dict_from_file.keys():
                dict_from_file["scrapetitle"] = None

            if "scrapelink" not in dict_from_file.keys():
                dict_from_file["scrapelink"] = None

            if "linkprecede" not in dict_from_file.keys():
                dict_from_file["linkprecede"] = None

            if "scrapebonus" not in dict_from_file.keys():
                dict_from_file["scrapebonus"] = None

            if "scrapebonussplit" not in dict_from_file.keys():
                dict_from_file["scrapebonussplit"] = None

            if "scrapetimezone" not in dict_from_file.keys():
                dict_from_file["scrapetimezone"] = "UTC"

        if comconf not in bot.memory['feeds'].keys():
            bot.memory['feeds'][comconf] = dict_from_file
