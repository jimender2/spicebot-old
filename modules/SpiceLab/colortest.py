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
from sopel.formatting import *


@sopel.module.commands('colortest')
def mainfunction(bot, trigger):
    bot.say(color("RED STRING", colors.RED))
    bot.say(bold("BOLD STRING"))
    bot.say(underline("UNDERLINED STRING"))
