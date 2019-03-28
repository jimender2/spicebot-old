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


@sopel.module.commands('tbf')
def mainfunction(bot, trigger):

    botcom = bot_module_prerun(bot, trigger)
    if not botcom.modulerun:
        return

    if not botcom.multiruns:
        execute_main(bot, trigger, botcom)
    else:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip.main(botcom.triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            botcom.triggerargsarray = spicemanip.main(command_split_partial, 'create')
            execute_main(bot, trigger, botcom)

    botdict_save(bot)


def execute_main(bot, trigger, botcom):

    myline = spicemanip.main(botcom.triggerargsarray, 0)
    fair = 'f'
    for letter in ['a', 'i', 'h', 'r']:
        rand = random.randint(1, 10)
        letter = str(letter) * rand
        fair = str(fair + letter)
    if not myline:
        message = "To be " + fair + "..."
    else:
        message = "To be " + fair + "; " + myline
    osd(bot, trigger.sender, 'say', message)
