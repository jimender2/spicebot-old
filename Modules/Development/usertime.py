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
import pytz
from tzlocal import get_localzone

# Ensure Encoding
reload(sys)
sys.setdefaultencoding('utf-8')

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
    date_str = "2018-12-13 22:28:15"
    datetime_obj_naive = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    datetime_obj_pacific = timezone('Pacific/Auckland').localize(datetime_obj_naive)
    datedisplaystring = str(datetime_obj_pacific.strftime("%Y-%m-%d %H:%M:%S %Z%z"))
    bot.say(datedisplaystring)
