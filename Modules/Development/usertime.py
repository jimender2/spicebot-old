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
# imports specific to this file
import datetime
import time
import pytz
import tzlocal

# Ensure Encoding
reload(sys)
sys.setdefaultencoding('utf-8')

# Creator details
comdict = {"author": "dysonparkes", "contributors": ["dysonparkes alone"]}
# user_timezone details
user_locale = {
                        "dysonparkes": "Pacific/Auckland",
                        "deathbybandaid": "US/Pacific"  # UTC -5
}


@sopel.module.commands('time')
def mainfunctionnobeguine(bot, trigger):
    """Confirm module is enabled."""
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
    """Do the thing."""
    UTC_Date = datetime.datetime.utcnow()
    instigator = trigger.nick
    newzone = user_locale.get(instigator)
    UTC_display = format_date(UTC_Date)
    #  datetime_obj_pacific = timezone('Pacific/Auckland').localize(datetime_obj_naive)
    #  datedisplaystring = datetime_obj_pacific.strftime("%Y-%m-%d %H:%M:%S %Z%z")
    message = "UTC is currently: " + UTC_display + ". " + target + " is in " + newzone + ", where the time is: " +
    bot.say(message)


def format_date(timestamp):
    """Manipulate date to match formatting"""
    Date_Format = "%Y-%m-%d %H:%M"
    newdatestring = datetime.datetime.strftime(timestamp, Date_Format)
    return newdatestring


def get_localtime(timestamp, newtimezone):
    """Convert datetime to local time."""
    localstamp = datetime.timezone(newtimezone).localize(timestamp)
    localtime = format_date(localstamp)
    return localtime
