#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *

GITWIKIURL = "https://github.com/deathbybandaid/SpiceBot/wiki"

@sopel.module.commands('help')
def mainfunction(bot, trigger):
    onscreentext(bot, ['say'], "Online Docs: " + GITWIKIURL)
