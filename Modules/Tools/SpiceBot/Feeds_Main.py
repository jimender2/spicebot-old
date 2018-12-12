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


@sopel.module.commands('feed', "feeds")
@sopel.module.thread(True)
def mainfunctionnobeguine(bot, trigger):

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

    valid_commands = ['enable', 'disable', 'reset', 'run', 'subscribe', 'unsubscribe']
    command = spicemanip(bot, [x for x in botcom.triggerargsarray if x in valid_commands], 1) or 'run'
    if command in botcom.triggerargsarray:
        botcom.triggerargsarray.remove(command)

    feed_select = spicemanip(bot, [x for x in botcom.triggerargsarray if x in bot.memory["botdict"]["tempvals"]['feeds'].keys() or x == 'all'], 1) or 'nofeed'
    if feed_select == 'nofeed':
        feed_list = spicemanip(bot, bot.memory["botdict"]["tempvals"]['feeds'].keys(), 'list')
        osd(bot, botcom.channel_current, 'say', "Valid Feeds are " + feed_list)
        return
    if feed_select == 'all':
        current_feed_list = bot.memory["botdict"]["tempvals"]['feeds'].keys()
    else:
        current_feed_list = []
        for word in botcom.triggerargsarray:
            if word in bot.memory["botdict"]["tempvals"]['feeds'].keys():
                current_feed_list.append(word)

    if command == 'run':
        for feed in current_feed_list:
            dispmsg = bot_dictcom_feeds_handler(bot, botcom, feed, True)
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
            feed_type = eval("feeds." + feed + ".type")
            if feed_type in ['rss', 'youtube', 'scrape', 'json']:
                newlist.append(feed)
        if newlist != []:
            for feed in newlist:
                reset_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildcurrent')
            osd(bot, botcom.channel_current, 'say', spicemanip(bot, newlist, 'list') + " " + hashave(newlist) + " been " + command + ".")
        else:
            osd(bot, botcom.channel_current, 'say', "No selected feeds to " + command + ".")
        return

    channelselect = spicemanip(bot, [x for x in botcom.triggerargsarray if x in bot.privileges.keys()], 1) or botcom.channel_current

    if command == 'enable':
        channelmodulesarray = get_nick_value(bot, channelselect, "long", "feeds", "enabled") or []
        newlist = []
        for feed in current_feed_list:
            if feed not in channelmodulesarray:
                newlist.append(feed)
        if newlist != []:
            adjust_nick_array(bot, channelselect, "long", "feeds", "enabled", newlist, "add")
            osd(bot, botcom.channel_current, 'say', spicemanip(bot, newlist, 'list') + " " + hashave(newlist) + " been " + command + "d for " + str(channelselect) + ".")
        else:
            osd(bot, botcom.channel_current, 'say', "No selected feeds to " + command + ".")
        return

    if command == 'disable':
        channelmodulesarray = get_nick_value(bot, channelselect, "long", "feeds", "enabled") or []
        newlist = []
        for feed in current_feed_list:
            if feed in channelmodulesarray:
                newlist.append(feed)
        if newlist != []:
            adjust_nick_array(bot, channelselect, "long", "feeds", "enabled", newlist, "del")
            osd(bot, botcom.channel_current, 'say', spicemanip(bot, newlist, 'list') + " " + hashave(newlist) + " been " + command + "d for " + str(channelselect) + ".")
        else:
            osd(bot, botcom.channel_current, 'say', "No selected feeds to " + command + ".")
        return
