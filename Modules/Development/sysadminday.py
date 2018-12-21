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

# Ensure Encoding
reload(sys)
sys.setdefaultencoding('utf-8')

comdict = {
            "author": "deathbybandaid",
            "contributors": [],
            "description": "",
            'privs': [],
            "example": "",
            "exampleresponse": "",
            }


@sopel.module.commands('sysadmin', 'sysadminday')
def mainfunctionnobeguine(bot, trigger):

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

    now = datetime.datetime.utcnow()
    now = datetime.datetime(now.year, now.month, now.day, 0, 0, 0, 0).replace(tzinfo=pytz.UTC)

    event = {
            "name": "SysAdmin day",
            "month": 7,
            "day": 27,
            "today": "Happy Sysadmin day",
            }

    entrytime = datetime.datetime(now.year, event["month"], event["day"], 0, 0, 0, 0).replace(tzinfo=pytz.UTC)
    entrytime = str(entrytime)
    entrytime = parser.parse(entrytime)

    timeuntil = (entrytime - now).total_seconds()
    if timeuntil == 0:
        nextyear = now + datetime.timedelta(days=365)
        nextime = humanized_time((entrytime - now).total_seconds()) + " from now"
        if event["today"]:
            timecompare = [event["today"], "(Next): " + nextime]
        else:
            timecompare = ["Right now", "(Next): " + nextime]
    elif timeuntil > 0:
        nextime = humanized_time((entrytime - now).total_seconds()) + " from now"
        lastyear = now - datetime.timedelta(days=365)
        previoustime = humanized_time((now - lastyear).total_seconds()) + " ago"
        timecompare = ["(Previous): " + previoustime, "(Next): " + nextime]
    else:
        previoustime = humanized_time((now - entrytime).total_seconds()) + " ago"
        nextyear = now + datetime.timedelta(days=365)
        nextime = humanized_time((entrytime - now).total_seconds()) + " from now"
        timecompare = ["(Previous): " + previoustime, "(Next): " + nextime]

    timecompare.insert(0, "[" + event["name"] + "]")

    osd(bot, botcom.channel_current, 'say', timecompare)
