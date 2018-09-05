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
    databasekey = 'guess'
    command = get_trigger_arg(bot, triggerargsarray, 1)
    message = sayingsmodule(bot, databasekey, triggerargsarray, command)
    osd(bot, trigger.sender, 'say', message)


def sayingsmodule(bot, databasekey, triggerargsarray, thingtodo):
    """Handle the creation and manipulation of modules that return sayings."""
    # add, remove, last, count, list, initialise?
    response = "Something went wrong. Oops."
    inputstring = get_trigger_arg(bot, triggerargsarray, '2+')
    existingarray = get_database_value(bot, bot.nick, databasekey) or []
    if thingtodo == "add":
        if inputstring not in existingarray:
            adjust_database_array(bot, bot.nick, inputstring, databasekey, 'add')
            response = "Added to database."
        else:
            response = "That is already in the database."
    elif thingtodo == "remove":
        if inputstring not in existingarray:
            response = "That was not found in the database."
        else:
            adjust_database_array(bot, bot.nick, inputstring, databasekey, 'del')
            response = "Removed from database."
    elif thingtodo == "count":
        messagecount = len(existingarray)
        response = "I guess there are currently " + str(messagecount) + " responses in the database."
    elif thingtodo == "last":
        response = get_trigger_arg(bot, existingarray, "last")
    else:
        response = get_trigger_arg(bot, existingarray, "random") or ''
        if response == '':
            response = "I'm afraid I couldn't find an entry for that."
    return response
