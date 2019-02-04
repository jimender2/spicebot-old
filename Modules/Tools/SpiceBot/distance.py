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
            "description": "A tool for converting distances",
            'privs': [],
            "example": ".distance 24 mile",
            "exampleresponse": "Instigator: 38.62km = 24.00 miles",
            }


"""
Based on the default units module.
"""


find_length = re.compile(r'([0-9]*\.?[0-9]*)[ ]*(mile[s]?|mi|inch|in|foot|feet|ft|yard[s]?|yd|(?:milli|centi|kilo|)meter[s]?|[mkc]?m|ly|light-year[s]?|au|astronomical unit[s]?|parsec[s]?|pc)', re.IGNORECASE)


@sopel.module.commands('length', 'distance', 'howfar')
@example('.distance 3m', '3.00m = 9 feet, 10.11 inches')
@example('.distance 3km', '3.00km = 1.86 miles')
@example('.distance 3 miles', '4.83km = 3.00 miles')
@example('.distance 3 inch', '7.62cm = 3.00 inches')
@example('.distance 3 feet', '91.44cm = 3 feet, 0.00 inches')
@example('.distance 3 yards', '2.74m = 9 feet, 0.00 inches')
@example('.distance 155cm', '1.55m = 5 feet, 1.02 inches')
@example('.length 3 ly', '28382191417742.40km = 17635876112814.77 miles')
@example('.length 3 au', '448793612.10km = 278867421.71 miles')
@example('.length 3 parsec', '92570329129020.20km = 57520535754731.61 miles')
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
    """Convert distances."""
    try:
        source = find_length.match(trigger.group(2)).groups()
    except (AttributeError, TypeError):
        bot.reply("That's not a valid length unit.")
        return NOLIMIT
    unit = source[1].lower()
    numeric = float(source[0])
    meter = 0
    if unit in ("meters", "meter", "m"):
        meter = numeric
    elif unit in ("millimeters", "millimeter", "mm"):
        meter = numeric / 1000
    elif unit in ("kilometers", "kilometer", "km"):
        meter = numeric * 1000
    elif unit in ("miles", "mile", "mi"):
        meter = numeric / 0.00062137
    elif unit in ("inch", "in"):
        meter = numeric / 39.370
    elif unit in ("centimeters", "centimeter", "cm"):
        meter = numeric / 100
    elif unit in ("feet", "foot", "ft"):
        meter = numeric / 3.2808
    elif unit in ("yards", "yard", "yd"):
        meter = numeric / (3.2808 / 3)
    elif unit in ("light-year", "light-years", "ly"):
        meter = numeric * 9460730472580800
    elif unit in ("astronomical unit", "astronomical units", "au"):
        meter = numeric * 149597870700
    elif unit in ("parsec", "parsecs", "pc"):
        meter = numeric * 30856776376340068

    if meter >= 1000:
        metric_part = '{:.2f}km'.format(meter / 1000)
    elif meter < 0.01:
        metric_part = '{:.2f}mm'.format(meter * 1000)
    elif meter < 1:
        metric_part = '{:.2f}cm'.format(meter * 100)
    else:
        metric_part = '{:.2f}m'.format(meter)

    # Shit like this makes glad I'm not an American.
    inch = meter * 39.37
    foot = int(inch) // 12
    inch = inch - (foot * 12)
    yard = foot // 3
    mile = meter * 0.000621371192

    if yard > 500:
        stupid_part = '{:.2f} miles'.format(mile)
    else:
        parts = []
        if yard >= 100:
            parts.append('{} yards'.format(yard))
            foot -= (yard * 3)

        if foot == 1:
            parts.append('1 foot')
        elif foot != 0:
            parts.append('{:.0f} feet'.format(foot))

        parts.append('{:.2f} inches'.format(inch))

        stupid_part = ', '.join(parts)

    bot.reply('{} = {}'.format(metric_part, stupid_part))
