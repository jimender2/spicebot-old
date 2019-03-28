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
import re

# Ensure Encoding
reload(sys)
sys.setdefaultencoding('utf-8')

comdict = {
            "author": "dysonparkes",
            "contributors": [],
            "description": "A tool for converting temperatures",
            'privs': [],
            "example": ".temp 100F",
            "exampleresponse": "Instigator: 37.78°C = 100.00°F = 310.93K",
            }


"""
Based on the default units module.
"""


find_temp = re.compile(r'(-?[0-9]*\.?[0-9]*)[ °]*(K|C|F)', re.IGNORECASE)


@sopel.module.commands('temp', 'temperature')
@example('.temp 100F', '37.78°C = 100.00°F = 310.93K')
@example('.temp 100C', '100.00°C = 212.00°F = 373.15K')
@example('.temp 100K', '-173.15°C = -279.67°F = 100.00K')
def mainfunction(bot, trigger):
    """Check to see if the module is enabled."""
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
    """Convert temperatures."""
    try:
        source = find_temp.match(trigger.group(2)).groups()
    except (AttributeError, TypeError):
        bot.reply("That's not a valid temperature.")
        return NOLIMIT
    unit = source[1].upper()
    numeric = float(source[0])
    celsius = 0
    if unit == 'C':
        celsius = numeric
    elif unit == 'F':
        celsius = f_to_c(numeric)
    elif unit == 'K':
        celsius = k_to_c(numeric)

    kelvin = c_to_k(celsius)
    fahrenheit = c_to_f(celsius)

    if kelvin >= 0:
        bot.reply("{:.2f}°C = {:.2f}°F = {:.2f}K".format(celsius, fahrenheit, kelvin))
    else:
        bot.reply("Physically impossible temperature.")
