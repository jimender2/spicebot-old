#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
from pyowm import OWM
import json

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
            "author": "jimender2",
            "contributors": [],
            "description": "version 1.0",
            'privs': [],
            "example": "",
            "exampleresponse": "",
            }


@sopel.module.commands('weather')
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
    owm = OWM(API_key="347db727b53caea97419c02f17f4fdf5", version='2.5')
#    obs = owm.weather_at_place('London,GB')

    try:
        location = spicemanip(bot, botcom.triggerargsarray, '1+') or ""
        if location == "":
            bot.say("Please tell me where you live")
            valid = False
        else:
            obs = owm.weather_at_place(location)
            valid = True
    except:
        bot.say("Sorry invalid location")
        valid = False

    if valid:
        w = obs.get_weather()
        t = w.get_wind()
        u = w.to_JSON()

        weather = json.loads(u)
#        osd(bot, botcom.channel_current, 'say', str(u))
        wind = weather["wind"]
        speed = str( wind["speed"] )
        status = str( weather["status"] )
        temp = weather["temperature"]
        high = temp["temp_max"]
        high = str((( 1.8 * (high - 273) + 32)))
        low = temp["temp_min"]
        low = str((( 1.8 * (low - 273) + 32)))
        temperature = temp["temp"]
        temperature = str((( 1.8 * (temperature - 273) + 32)))

        string = botcom.instigator + " the weather at " + location + " is as follows:"
        bot.say(str(string))

        string = status + " with a current temperature of " + temperature + " degrees.  The high is " + high + " and the low is " + low + ". The wind is blowing at " + speed + " miles an hour."
        bot.say(string)
