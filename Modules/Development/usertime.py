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
User_locale = {
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
    Date_Format = "%Y-%m-%d %H:%M:%S"
    UTC_Date = datetime.datetime.utcnow()
    UTC_DateString = str(UTC_Date)
    #datetime_obj_naive = datetime.datetime.strptime(UTC_DateString, Date_Format)
    datetime_obj_naive = parse_prefix(UTC_Date, Date_Format)
    #  datetime_obj_pacific = timezone('Pacific/Auckland').localize(datetime_obj_naive)
    #  datedisplaystring = datetime_obj_pacific.strftime("%Y-%m-%d %H:%M:%S %Z%z")
    bot.say(datetime_obj_naive)


def parse_prefix(dateline, fmt):
    """Make datetime look nice"""
    cover = len(datetime.datetime.utcnow().strftime(fmt))
    return datetime.strptime(line[:cover], fmt)
