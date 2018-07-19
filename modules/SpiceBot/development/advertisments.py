#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import requests
from lxml import html
import calendar
import arrow
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# author jimender2

testarray = ["doubled recommends these new drapes https://goo.gl/BMTMde",
             "Spiceduck for spicerex mascot 2k18",
             "Deathbybandaid is looking for developers for spicebot and spicethings"]

databasekey = 'ads'

hardcoded_not_in_this_chan = ["#spiceworks"]


@sopel.module.commands('ads', 'advertisements', 'ad', 'advertisement')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger,'ads')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    instigator = trigger.nick
    inchannel = trigger.sender

    database_initialize(bot, bot.nick, testarray, databasekey)

    command = get_trigger_arg(bot, triggerargsarray, 1)
    inputstring = get_trigger_arg(bot, triggerargsarray, '2+')
    existingarray = get_database_value(bot, bot.nick, databasekey) or []
    if command == "add":
        if inputstring not in existingarray:
            adjust_database_array(bot, bot.nick, inputstring, databasekey, 'add')
            message = "Added to database."
            osd(bot, trigger.sender, 'say', message)
        else:
            message = "That response is already in the database."
            osd(bot, trigger.sender, 'say', message)
    elif command == "remove":
        if inputstring not in existingarray:
            message = "That response was not found in the database."
            osd(bot, trigger.sender, 'say', message)
        else:
            adjust_database_array(bot, bot.nick, inputstring, databasekey, 'del')
            message = "Removed from database."
            osd(bot, trigger.sender, 'say', message)
    elif command == "count":
        messagecount = len(existingarray)
        message = "There are currently " + str(messagecount) + " ads in the database."
        osd(bot, trigger.sender, 'say', message)

    elif command == "last":
        message = get_trigger_arg(bot, existingarray, "last")
        osd(bot, trigger.sender, 'say', message)

    else:
        message = get_trigger_arg(bot, existingarray, "random") or ''
        if message == '':
            message = "No response found. Have any been added?"
        osd(bot, trigger.sender, 'say', message)


def get_database_value(bot, nick, databasekey):
    databasecolumn = str(databasekey)
    database_value = bot.db.get_nick_value(nick, databasecolumn) or 0
    return database_value


def database_initialize(bot, nick, array, database):
    databasekey = str(database)
    existingarray = get_database_value(bot, bot.nick, databasekey)
    if not existingarray:
        arraycount = (len(array) - 1)
        i = 0
        while (i <= arraycount):
            inputstring = array[i]
            adjust_database_array(bot, bot.nick, inputstring, databasekey, 'add')
            i = i + 1


@sopel.module.interval(60)
def advertisement(bot):
    databasekey = 'ads'
    existingarray = get_database_value(bot, bot.nick, databasekey) or []
    message = get_trigger_arg(bot, existingarray, "random") or ''
    if not message:
        message = "Spiceduck for Spiceworks mascot 2k18"
    for channel in bot.channels:
        if channel not in hardcoded_not_in_this_chan:
            osd(bot, channel, 'say', message)
