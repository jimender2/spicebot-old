#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import os
import sys
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

commandarray = ["add","remove"]
#count, list?

@sopel.module.commands('fix')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    instigator = trigger.nick
    command = get_trigger_arg(triggerargsarray, 1)
    fixstring = get_trigger_arg(triggerargsarray, '2+')
    existingfixarray = get_botdatabase_value(bot, bot.nick, 'fixes')
    if command in commandarray:
        #bot.say("Command detected")
        if command == "add":
            if fixstring in existingfixarray:
                message = "That's already in the array"
            else:
                adjust_botdatabase_array(bot, bot.nick, fixstring, 'fixes', 'add')
                message = fixstring + " added to database."
        if subcommand == "remove":
            if fixstring in existingfixarray:
                adjust_botdatabase_array(bot, bot.nick, fixstring, 'fixes', 'del')
                message = fixstring + " removed from database."
            else:
                message = fixstring + " not found in database."
    else:
        message = "No string found"
    bot.say(message)
