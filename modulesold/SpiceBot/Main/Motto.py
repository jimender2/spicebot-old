#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
import random
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# author jimender2

databasekey = 'motto'


@sopel.module.commands('motto', 'tag', 'flair')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'motto')
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    instigator = trigger.nick
    inchannel = trigger.sender

    command = spicemanip(bot, triggerargsarray, 1)
    inputstring = spicemanip(bot, triggerargsarray, '2+')
    existingarray = get_database_value(bot, instigator, databasekey) or []
    if command == "add":
        if inputstring not in existingarray:
            adjust_database_array(bot, instigator, inputstring, databasekey, 'add')
            message = "Added to your flair list."
            osd(bot, trigger.sender, 'say', message)
        else:
            message = "You already have that in your flair list."
            osd(bot, trigger.sender, 'say', message)
    elif command == "remove":
        if inputstring not in existingarray:
            message = "That response was not found in your flair list."
            osd(bot, trigger.sender, 'say', message)
        else:
            adjust_database_array(bot, instigator, inputstring, databasekey, 'del')
            message = "Removed from database."
            osd(bot, trigger.sender, 'say', message)
    elif command == "count":
        messagecount = len(existingarray)
        message = "There are currently " + str(messagecount) + " mottos in the database."
        osd(bot, trigger.sender, 'say', message)
    elif command == "last":
        message = spicemanip(bot, existingarray, "last")
        osd(bot, trigger.sender, 'say', message)

    else:
        motto = spicemanip(bot, existingarray, "random") or 'You have no flair. Add some now!!'
        osd(bot, trigger.sender, 'say', motto)


def get_database_value(bot, nick, databasekey):
    databasecolumn = str(databasekey)
    database_value = bot.db.get_nick_value(nick, databasecolumn) or 0
    return database_value
