#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# author jimender2


@sopel.module.commands('guess')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    instigator = trigger.nick
    inchannel = trigger.sender
    databasekey = 'guess'
    command = get_trigger_arg(bot, triggerargsarray, 1)
    inputstring = get_trigger_arg(bot, triggerargsarray, '2+')
    existingarray = get_database_value(bot, bot.nick, databasekey) or []
    if command == "add":
        if inputstring not in existingarray:
            adjust_database_array(bot, bot.nick, inputstring, databasekey, 'add')
            message = "Added to database."
        else:
            message = "That is already in the database."
    elif command == "remove":
        if inputstring not in existingarray:
            message = "That was not found in the database."
        else:
            adjust_database_array(bot, bot.nick, inputstring, databasekey, 'del')
            message = "Removed from database."
    elif command == "count":
        messagecount = len(existingarray)
        message = "I guess there are currently " + str(messagecount) + " responses in the database."
    elif command == "last":
        message = get_trigger_arg(bot, existingarray, "last")
    else:
        message = get_trigger_arg(bot, existingarray, "random") or ''
        if message == '':
            message = "No response found. I guess none have been added."
    osd(bot, trigger.sender, 'say', message)
