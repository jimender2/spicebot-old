#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel.module

# imports for system and OS access, directories
import os
import sys

# imports based on THIS file
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# Ensure Encoding
reload(sys)
sys.setdefaultencoding('utf-8')


"""
@sopel.module.interval(1800)
@sopel.module.thread(True)
def autosave(bot):

    if not bot_startup_requirements_met(bot, ["botdict", "monologue"]):
        return

    botdict_save(bot)
    """


@event('001')
@rule('.*')
@sopel.module.thread(True)
def savingitall(bot, trigger):

    # don't run jobs if not ready
    while not bot_startup_requirements_met(bot, ["botdict", "monologue"]):
        pass

    while True:
        time.sleep(1800)
        botdict_save(bot)
