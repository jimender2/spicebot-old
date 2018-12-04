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


@sopel.module.commands('seen')
@sopel.module.thread(True)
def seen(bot, trigger):

    botcom = bot_module_prerun(bot, trigger)
    if not botcom.modulerun:
        return

    if "sock_bot_list" not in bot.memory:
        bot.memory["sock_bot_list"] = []

    posstarget = spicemanip(bot, botcom.triggerargsarray, 1) or 0
    if not posstarget:
        return osd(bot, botcom.channel_current, 'say', ".seen <nick> - Reports when <nick> was last seen.")
    elif bot_check_inlist(bot, posstarget, [str(bot.nick)]):
        return osd(bot, botcom.channel_current, 'say', "I'm right here!")
    elif bot_check_inlist(bot, posstarget, bot.memory["botdict"]["tempvals"]['bots_list'].keys()) or bot_check_inlist(bot, posstarget, bot.memory["sock_bot_list"]):
        return osd(bot, botcom.channel_current, 'say', "I don't spy on the other bots!")
    elif bot_check_inlist(bot, posstarget, [str(botcom.instigator)]):
        return osd(bot, botcom.channel_current, 'say', "You're right there!")

    lastseen = []

    # current bot
    if str(posstarget) in bot.memory["botdict"]["users"].keys():
        if 'user_activity' in bot.memory["botdict"]["users"][str(posstarget)].keys():
            if 'list' in bot.memory["botdict"]["users"][str(posstarget)]['user_activity'].keys():
                lastseenrecord = bot.memory["botdict"]["users"][str(posstarget)]['user_activity']['list']
                if lastseenrecord != []:
                    lastseen.append(lastseenrecord[-1])

    # other bots
    otherbots = bot_api_get_users(bot)
    otherbotmatchcur = []
    otherbotmatch = []
    for host in otherbots.keys():
        for bots in otherbots[host].keys():
            if str(bots) not in bot.memory["sock_bot_list"]:
                bot.memory["sock_bot_list"].append(str(bots))
            if bot_check_inlist(bot, posstarget, otherbots[host][bots]['users'].keys()):
                otherbotmatch.append(nick_actual(bot, posstarget, otherbots[host][bots]['users'].keys()))
                if bot_check_inlist(bot, posstarget, otherbots[host][bots]['all_current_users']):
                    otherbotmatchcur.append(nick_actual(bot, posstarget, otherbots[host][bots]['users'].keys()))
                if str(posstarget) in otherbots[host][bots]["users"].keys():
                    if 'user_activity' in otherbots[host][bots]["users"][str(posstarget)].keys():
                        if 'list' in otherbots[host][bots]["users"][str(posstarget)]['user_activity'].keys():
                            lastseenrecord = otherbots[host][bots]["users"][str(posstarget)]['user_activity']['list']
                            if lastseenrecord != []:
                                lastseen.append(lastseenrecord[-1])

    if lastseen == []:
        return osd(bot, botcom.channel_current, 'say', "Sorry, the network of SpiceBots have never seen " + str(posstarget) + " around.")

    seentime = None
    entrynumber, winningentry = 0, 0
    for seenrecord in lastseen:
        if not seentime:
            seentime = seenrecord["time"]
            winningentry = entrynumber
        elif seenrecord["time"] > seentime:
            seentime = seenrecord["time"]
            winningentry = entrynumber
        entrynumber += 1
    lastseenwinner = lastseen[winningentry]

    if str(posstarget) in bot.memory["botdict"]["users"].keys():
        posstarget = nick_actual(bot, posstarget)
    else:
        posstarget = nick_actual(bot, posstarget, otherbotmatch)

    howlongago = humanized_time(time.time() - lastseenwinner["time"])

    intent = 'saying'
    if "intent" in lastseenwinner.keys():
        if lastseenwinner["intent"]:
            if lastseenwinner["intent"]:
                intent = "doing /me"

    if bot_check_inlist(bot, posstarget, bot.memory["botdict"]["tempvals"]['all_current_users']) or bot_check_inlist(bot, posstarget, otherbotmatchcur):
        osd(bot, botcom.channel_current, 'say', str(posstarget) + " is online right now and was last seen " + str(howlongago).strip() + " ago by " + str(lastseenwinner["bot_eyes"]) + " on " + str(lastseenwinner["server"]) + " in " + str(lastseenwinner["channel"]) + " " + intent + " " + str(lastseenwinner["spoken"]))
    else:
        osd(bot, botcom.channel_current, 'say', str(posstarget) + " was last seen " + str(howlongago).strip() + " ago on " + str(lastseenwinner["server"]) + " in " + str(lastseenwinner["channel"]) + " by " + str(lastseenwinner["bot_eyes"]) + " " + intent + " " + str(lastseenwinner["spoken"]))
