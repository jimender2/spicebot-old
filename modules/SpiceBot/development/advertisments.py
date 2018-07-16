#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import requests
from lxml import html
import datetime
from time import strptime
from dateutil import parser
import calendar
import arrow
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# author jimender2

testarray = ["test1", "test2", "test3", "test4", "test5",]

commandarray = ["add","remove","count", "last"]


@sopel.module.commands('ads', 'advertisements', 'ad', 'advertisement')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger,'ads')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)


def execute_main(bot, trigger, triggerargsarray):
    instigator = trigger.nick
    inchannel = trigger.sender

    databasekey = 'ads'

    database_initialize(bot, bot.nick, testarray, databasekey)

    command = get_trigger_arg(bot, triggerargsarray, 1)
    inputstring = get_trigger_arg(bot, triggerargsarray, '2+')
    existingarray = get_database_value(bot, bot.nick, databasekey) or []
    if command in commandarray:
        if command == "add":
            if inputstring not in existingarray:
                adjust_database_array(bot, bot.nick, inputstring, databasekey, 'add')
                message = "Added to database."
                bot.say(message)
            else:
                message = "That response is already in the database."
                bot.say(message)
        elif command == "remove":
            if inputstring not in existingarray:
                message = "That response was not found in the database."
                bot.say(message)
            else:
                adjust_database_array(bot, bot.nick, inputstring, databasekey, 'del')
                message = "Removed from database."
                bot.say(message)
        elif command == "count":
            messagecount = len(existingarray)
            message = "There are currently " + str(messagecount) + " ads in the database."
            bot.say(message)

        elif command == "last":
            message = get_trigger_arg(bot, existingarray, "last")
            bot.say(message)
    else:
        message = get_trigger_arg(bot, existingarray, "random") or ''
        if message == '':
            message = "No response found. Have any been added?"
        bot.say(message)


def get_database_value(bot, nick, databasekey):
    databasecolumn = str(databasekey)
    database_value = bot.db.get_nick_value(nick, databasecolumn) or 0
    return database_value


def database_initialize(bot, nick, array, database):
    databasekey = str(database)
    existingarray = get_database_value(bot, bot.nick, databasekey)
    if not existingarray:
        arraycount = len(array)
        bot.say("entered")
        i = 0
        while (i <= arraycount):
            inputstring = array[i]
            adjust_database_array(bot, bot.nick, inputstring, databasekey, 'add')
            i = i + 1
            bot.say("test")


@sopel.module.interval(60)
def advertisement(bot):
    databasekey = 'ads'
    existingarray = get_database_value(bot, bot.nick, databasekey) or []
    message = get_trigger_arg(bot, existingarray, "random") or ''
    if message == '':
        message = "Spiceduck for Spiceworks mascot 2k18"
    bot.say(message)
