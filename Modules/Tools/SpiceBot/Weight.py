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
            "description": "A tool for converting weights",
            'privs': [],
            "example": ".weight 24 kg",
            "exampleresponse": "Instigator: 24.00kg = 52 pounds 14.58 ounces",
            }


"""
Based on the default units module.
"""


find_mass = re.compile(r'([0-9]*\.?[0-9]*)[ ]*(lb|lbm|pound[s]?|ounce|oz|(?:kilo|)gram(?:me|)[s]?|[k]?g)', re.IGNORECASE)


@sopel.module.commands('weight', 'mass')
def mainfunction(bot, trigger):
    """Check to see if the module is enabled."""
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
    """Convert mass."""
    try:
        source = find_mass.match(trigger.group(2)).groups()
    except (AttributeError, TypeError):
        bot.reply("That's not a valid mass unit.")
        return NOLIMIT
    unit = source[1].lower()
    numeric = float(source[0])
    metric = 0
    if unit in ("gram", "grams", "gramme", "grammes", "g"):
        metric = numeric
    elif unit in ("kilogram", "kilograms", "kilogramme", "kilogrammes", "kg"):
        metric = numeric * 1000
    elif unit in ("lb", "lbm", "pound", "pounds"):
        metric = numeric * 453.59237
    elif unit in ("oz", "ounce"):
        metric = numeric * 28.35

    if metric >= 1000:
        metric_part = '{:.2f}kg'.format(metric / 1000)
    else:
        metric_part = '{:.2f}g'.format(metric)

    ounce = metric * .035274
    pound = int(ounce) // 16
    ounce = ounce - (pound * 16)

    if pound > 1:
        stupid_part = '{} pounds'.format(pound)
        if ounce > 0.01:
            stupid_part += ' {:.2f} ounces'.format(ounce)
    else:
        stupid_part = '{:.2f} oz'.format(ounce)

    bot.reply('{} = {}'.format(metric_part, stupid_part))
