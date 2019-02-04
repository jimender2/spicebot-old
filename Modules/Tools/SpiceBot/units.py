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


find_mass = re.compile(r'([0-9]*\.?[0-9]*)[ ]*(lb|lbm|pound[s]?|ounce|oz|(?:kilo|)gram(?:me|)[s]?|[k]?g)', re.IGNORECASE) #


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
