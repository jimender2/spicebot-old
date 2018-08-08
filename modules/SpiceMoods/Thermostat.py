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
        osd(bot, trigger.sender, 'say', "The current temperature in " + botcom.channel_current + " is " + str(currenttemp) + " degrees " + str(currenttemp_type) + ".")
        return
