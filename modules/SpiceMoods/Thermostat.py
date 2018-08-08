#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *

# author deathbybandaid

temp_scales_disp = ['Kelvin', 'Celsius', 'Fahrenheit', 'Rankine', 'Rømer', 'Newton', 'Delisle', 'Réaumur']
temp_scales = ['kelvin', 'celsius', 'fahrenheit', 'rankine', 'romer', 'newton', 'delisle', 'reaumur']
temp_scales_short = ['K', 'C', 'F', 'Ra', 'Rø', 'N', 'D', 'Ré']


@sopel.module.commands('thermostat')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):

    validtempcommands = ['check', 'change', 'set']
    tempcommand = get_trigger_arg(bot, [x for x in triggerargsarray if x in validtempcommands], 1) or 'check'

    currenttemp = get_database_value(bot, botcom.channel_current, 'temperature') or 32
    currenttemp_type = get_database_value(bot, botcom.channel_current, 'temperature_type') or 'fahrenheit'

    if tempcommand == 'check':
        osd(bot, trigger.sender, 'say', "The current temperature in " + botcom.channel_current + " is " + str(currenttemp) + "° " + str(currenttemp_type) + ".")
        return

    if tempcommand in ['change', 'set']:
        degree = 450
        for original in temp_scales:
            for desired in temp_scales:
                bot.say(original + ": " + str(degree) + "     " + desired + str(temperature(bot, degree, original, desired)))


def temperature(bot, degree, original, desired):
    temperature = 0

    if original != 'kelvin':
        kelvin = eval(str(original.lower() + "_to_kelvin(bot, degree)"))
    else:
        kelvin = degree

    if desired != 'kelvin':
        temperature = eval("kelvin_to_" + str(desired.lower() + "(bot, degree)"))
    else:
        temperature = kelvin

    return temperature


"""
Celsius
"""


def celsius_to_kelvin(bot, degree):
    celsius = float(degree)
    kelvin = (celsius + 273)
    return kelvin


def kelvin_to_celsius(bot, degree):
    kelvin = float(degree)
    celsius = (kelvin - 273)
    return celsius


"""
Fahrenheit
"""


def fahrenheit_to_kelvin(bot, degree):
    fahrenheit = float(degree)
    kelvin = ((5/9) * (fahrenheit - 32) + 273)
    return kelvin


def kelvin_to_fahrenheit(bot, degree):
    kelvin = float(degree)
    fahrenheit = (1.8 * (kelvin - 273) + 32)
    return fahrenheit


"""
Rankine
"""


def rankine_to_kelvin(bot, degree):
    rankine = float(degree)
    kelvin = (rankine * (5/9))
    return kelvin


def kelvin_to_rankine(bot, degree):
    kelvin = float(degree)
    rankine = (kelvin * (9/5))
    return rankine


"""
Delisle
"""


def delisle_to_kelvin(bot, degree):
    delisle = float(degree)
    kelvin = (373 - (delisle * (2/3)))
    return kelvin


def kelvin_to_delisle(bot, degree):
    kelvin = float(degree)
    delisle = ((373 - kelvin) * (3/2))
    return delisle


"""
Newton
"""


def newton_to_kelvin(bot, degree):
    newton = float(degree)
    kelvin = (newton * (100/33) + 273)
    return kelvin


def kelvin_to_newton(bot, degree):
    kelvin = float(degree)
    newton = ((kelvin - 273) * (33/100))
    return newton


"""
Reaumur
"""


def reaumur_to_kelvin(bot, degree):
    reaumur = float(degree)
    kelvin = (reaumur * (5/4) + 273)
    return kelvin


def kelvin_to_reaumur(bot, degree):
    kelvin = float(degree)
    reaumur = ((kelvin - 273) * (4/5))
    return reaumur


"""
Romer
"""


def romer_to_kelvin(bot, degree):
    romer = float(degree)
    kelvin = ((romer - 7.5) * (40/21) + 273)
    return kelvin


def kelvin_to_romer(bot, degree):
    kelvin = float(degree)
    romer = ((kelvin - 273) * (21/40) + 7.5)
    return romer
