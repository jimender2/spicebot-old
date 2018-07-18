#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


from sopel.formatting import *


@sopel.module.commands('colortest')
def mainfunction(bot, trigger):
  osd(bot, trigger.sender, 'say', "normal text")
  osd(bot, trigger.sender, 'say', bold("bold text"))
  osd(bot, trigger.sender, 'say', "\x0309,01Color STRING\x03")
