# coding=utf-8
"""
units.py - Unit conversion module for Sopel
Copyright © 2013, Elad Alfassa, <elad@fedoraproject.org>
Copyright © 2013, Dimitri Molenaars, <tyrope@tyrope.nl>
Licensed under the Eiffel Forum License 2.
"""
from __future__ import unicode_literals, absolute_import, print_function, division

from sopel.module import commands, example, NOLIMIT
import re
from BotShared import *


find_length = re.compile(r'([0-9]*\.?[0-9]*)[ ]*(mile[s]?|mi|inch|in|foot|feet|ft|yard[s]?|yd|(?:milli|centi|kilo|)meter[s]?|[mkc]?m|ly|light-year[s]?|au|astronomical unit[s]?|parsec[s]?|pc)', re.IGNORECASE)
find_mass = re.compile(r'([0-9]*\.?[0-9]*)[ ]*(lb|lbm|pound[s]?|ounce|oz|(?:kilo|)gram(?:me|)[s]?|[k]?g)', re.IGNORECASE)

@commands('length', 'distance')
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
def distance(bot, trigger):
    """
    Convert distances
    """
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

    # Shit like this makes me hate being an American.
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


@commands('weight', 'mass')
def mass(bot, trigger):
    """
    Convert mass
    """
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


# if __name__ == "__main__":
#     from sopel.test_tools import run_example_tests
# run_example_tests(__file__)
