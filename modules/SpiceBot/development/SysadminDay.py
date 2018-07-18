#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
import datetime
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('sysadmin','sysadminday')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'sysadmin')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    today = datetime.datetime.now().strftime("%m/%d/%Y")
    day = "07/27/2018"
    day = day.rstrip('\n')
    day = day.rstrip('\r')
    day = day.rstrip()
    sysadminday = datetime.datetime.strptime(day, '%m/%d/%Y')
    if sysadminday > today:
        daystillsysadminday = sysadminday - today
        message = "There are " + daystillsysadminday + " till sysadminday"
    elif sysadminday < today:
        message = "We passed sysadmin day"
    else:
        message = "Happy Sysadmin day"
    bot.say(message)
