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

    # if "sock_bot_list" not in bot.memory:
    #    bot.memory["sock_bot_list"] = []

    posstarget = spicemanip(bot, botcom.triggerargsarray, 1) or 0
    if not posstarget:
        return osd(bot, botcom.channel_current, 'say', ".seen <nick> - Reports when <nick> was last seen.")
    elif bot_check_inlist(bot, posstarget, [str(bot.nick)]):
        return osd(bot, botcom.channel_current, 'say', "I'm right here!")
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

    if lastseen == []:
        return osd(bot, botcom.channel_current, 'say', "Sorry, I have never seen " + str(posstarget) + " around.")

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

    message = str(posstarget)
    if lastseenwinner["server"] == botcom.server:
        if bot_check_inlist(bot, posstarget, bot.memory["botdict"]["tempvals"]["servers_list"][botcom.server]['all_current_users']):
            message = str(message + " is online right now,")
    else:
        nada = 5
        # this is where we will check if user is active on another server

    message = str(message + " was last seen " + str(howlongago) + ",")

    if str(lastseenwinner["bot_eyes"]) != str(bot.nick):
        message = str(message + " by " + str(lastseenwinner["bot_eyes"]) + ",")

    if lastseenwinner["server"] != botcom.server:
        message = str(message + " on " + str(lastseenwinner["server"]) + ",")

    if lastseenwinner["channel"] != botcom.channel_current:
        message = str(message + " in " + str(lastseenwinner["channel"]) + ",")
    else:
        message = str(message + " in here,")

    intent = 'saying'
    posscom = spicemanip(bot, str(lastseenwinner["spoken"]), 1)
    if str(posscom).startswith("."):
        posscom = posscom.lower()[1:]
        if posscom in bot.memory["botdict"]["tempvals"]['all_coms']:
            intent = "running"
            spoken = str(posscom)
    elif "intent" in lastseenwinner.keys():
        if lastseenwinner["intent"]:
            if lastseenwinner["intent"]:
                intent = "doing /me"
    message = str(message + " " + intent + " " + str(lastseenwinner["spoken"]))

    osd(bot, botcom.channel_current, 'say', message)
