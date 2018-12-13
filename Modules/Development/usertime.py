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
                        "dysonparkes": "+12",
                        "deathbybandaid": "-5"
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
    tz = get_localzone()
    local_dt = tz.localize(datetime(2010, 4, 27, 12, 0, 0, 0), is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)  # NOTE: utc.normalize() is unnecessary here
    bot.say(str(utc_dt))
