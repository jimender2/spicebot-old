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


array = ["jump off a bridge"]


@sopel.module.commands('idea', 'goodidea, =')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'idea')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    osd(bot, trigger.sender, 'say', "do the thing")
    command = get_trigger_arg(bot, triggerargsarray, 1)
    inputstring = get_trigger_arg(bot, triggerargsarray, '2+')

    if command == 'good':
        if not inputstring:
            good()
        else:
            existingarray = get_database_value(bot, bot.nick, 'idea') or []
            if inputstring not in existingarray:
                adjust_database_array(bot, bot.nick, inputstring, 'idea', 'add')
                message = ""
                osd(bot, trigger.sender, 'say', message)


def good():
    database_initialize(bot, bot.nick, testarray, 'idea')
    existingarray = get_database_value(bot, bot.nick, 'idea') or []
    idea = get_trigger_arg(bot, existingarray, "random") or ''
