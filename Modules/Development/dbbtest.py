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
shareddir = os.path.dirname(os.path.dirname(__file__))
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

# from pip._internal.utils.misc import get_installed_distributions
import pkg_resources


@sopel.module.commands('dbbtest', 'deathbybandaidtest')
def mainfunction(bot, trigger):

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
    bot.say("DBB Testing")

    osd(bot, botcom.channel_current, 'say', 'Generating list of installed pip modules.')

    # pipinstalled = sorted(["%s" % (i.key) for i in get_installed_distributions()])
    # pipinstalled = sys.modules.keys()
    pipinstalled = sorted(["%s" % (i.key for i in [str(d).replace("", "==") for d in pkg_resources.working_set])])
    osd(bot, botcom.channel_current, 'say', str(pipinstalled))
