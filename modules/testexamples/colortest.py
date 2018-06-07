#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *


from sopel.formatting import *


@sopel.module.commands('colortest')
def mainfunction(bot, trigger):
  bot.say("normal text")
  bot.say(bold("bold text"))
  bot.say("RED STRING", colors.RED)
