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
    now = now.replace(tzinfo=pytz.UTC)

    entrytime = datetime.datetime(now.year, 7, 27, now.hour, now.minute, 0, 0).replace(tzinfo=pytz.UTC)
    entrytime = str(entrytime)
    entrytime = parser.parse(entrytime)

    timeuntil = (entrytime - now).total_seconds()
    if timeuntil == 0:
        timecompare = str("Right now")
    elif timeuntil > 0:
        timecompare = humanized_time((entrytime - now).total_seconds())
        timecompare = str(timecompare + " from now")
    else:
        timecompare = humanized_time((now - entrytime).total_seconds())
        timecompare = str(timecompare + " ago")

    osd(bot, trigger.sender, 'say', timecompare)

    return

    today = datetime.datetime.now()
    sysadminday = datetime.datetime.strptime('Jul 27 2018', '%b %d %Y')
    if sysadminday > today:
        daystillsysadminday = sysadminday - today
        message = "There are " + str(daystillsysadminday.days) + " days till SysAdmin day"
    elif sysadminday < today:
        daystillsysadminday = sysadminday - today
        message = "SysAdmin day happened " + str(daystillsysadminday.days) + " ago."
    else:
        message = "Happy Sysadmin day"
    osd(bot, trigger.sender, 'say', message)
