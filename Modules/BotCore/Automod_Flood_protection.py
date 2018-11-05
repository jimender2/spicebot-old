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
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *

# Ensure Encoding
reload(sys)
sys.setdefaultencoding('utf-8')


@rule('(.*)')
@sopel.module.thread(True)
def antiflood(bot, trigger):

    if "botdict_loaded" not in bot.memory:
        bot_saved_jobs_process(bot, trigger, 'bot_automod_flood')
        return

    bot_automod_flood_run(bot, trigger)


def bot_automod_flood_run(bot, trigger):

    # botcom dynamic Class
    botcom = class_create('botcom')
    botcom.default = 'botcom'

    # instigator
    botcom.instigator = trigger.nick

    # channel
    botcom.channel_current = trigger.sender

    if not botcom.channel_current.startswith("#"):
        return

    # Bots can't run commands
    if botcom.instigator in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
        return

    if bot.memory["botdict"]["tempvals"]['automod']["antiflood"] == []:
        bot.memory["botdict"]["tempvals"]['automod']["antiflood"].append({"nick": trigger.nick, "message": str(trigger)})
        return

    # only track the last 10 items
    if len(bot.memory["botdict"]["tempvals"]['automod']["antiflood"]) >= 10:
        bot.memory["botdict"]["tempvals"]['automod']["antiflood"] = spicemanip(bot, bot.memory["botdict"]["tempvals"]['automod']["antiflood"], '2+', 'return')

    lastnick = spicemanip(bot, bot.memory["botdict"]["tempvals"]['automod']["antiflood"], 'last', 'return')["nick"]
    if lastnick != botcom.instigator:
        bot.memory["botdict"]["tempvals"]['automod']["antiflood"].append({"nick": trigger.nick, "message": str(trigger)})
        return

    bot.memory["botdict"]["tempvals"]['automod']["antiflood"].append({"nick": trigger.nick, "message": str(trigger)})

    # Flooding is 5 lines in a row by the same person or 3 identical lines
    totalrecords = len(bot.memory["botdict"]["tempvals"]['automod']["antiflood"])
    if totalrecords < 3:
        return

    identicalcheck = totalrecords - 3
    messages = []
    osd(bot, botcom.instigator, 'notice', str(identicalcheck) + " " + str(int(totalrecords) + 1))
    for i in range(identicalcheck, totalrecords):
        currentdict = spicemanip(bot, bot.memory["botdict"]["tempvals"]['automod']["antiflood"], int(i + 1), 'return')
        messages.append(str(currentdict["message"]))

    identicalnumber = countX(messages, bot.memory["botdict"]["tempvals"]['automod']["antiflood"])
    if identicalnumber == 3:
        osd(bot, botcom.instigator, 'notice', "possible flooding")

    osd(bot, botcom.instigator, 'notice', str(len(messages)))
    osd(bot, botcom.instigator, 'notice', str(messages))

    # if totalrecords >= 5:
    return

    # vars
    channel = trigger.sender
    currentmessage = trigger.group(1)

    # Flooding is 5 lines in a row by the same person or 3 identical lines
    floodyell = 0
    antifloodwarning = str(instigator + ", please do not flood the channel.")
    lastnicksubmit = get_database_value(bot, channel, 'automod_antifloodnick') or bot.nick
    if lastnicksubmit != instigator:
        set_database_value(bot, channel, 'automod_antifloodnick', instigator)
        set_database_value(bot, channel, 'automod_antifloodcount', 1)
        set_database_value(bot, channel, 'automod_antifloodnickwarned', None)
        set_database_value(bot, channel, 'automod_antifloodmessage', currentmessage)
        set_database_value(bot, channel, 'automod_antifloodmessagecount', 1)
    else:
        lastmessage = get_database_value(bot, channel, 'automod_antifloodmessage') or ''
        if currentmessage != lastmessage:
            set_database_value(bot, channel, 'automod_antifloodmessage', currentmessage)
            set_database_value(bot, channel, 'automod_antifloodmessagecount', 1)
        else:
            adjust_database_value(bot, channel, 'automod_antifloodmessagecount', 1)
            getcurrentmessagecount = get_database_value(bot, channel, 'automod_antifloodmessagecount') or 1
            if int(getcurrentmessagecount) >= 3:
                floodyell = 1
        lastnicksubmit = get_database_value(bot, channel, 'automod_antifloodnick') or bot.nick
        adjust_database_value(bot, channel, 'automod_antifloodcount', 1)
        getcurrentcount = get_database_value(bot, channel, 'automod_antifloodcount') or 1
        if int(getcurrentcount) > 5:
            floodyell = 1
    lastnicksubmitwarned = get_database_value(bot, channel, 'automod_antifloodnickwarned') or bot.nick
    if lastnicksubmitwarned != instigator and floodyell:
        set_database_value(bot, channel, 'automod_antifloodnickwarned', instigator)
        osd(bot, channel, 'action', antifloodwarning)
