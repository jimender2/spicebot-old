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
This Cycles through all of the dictionary commands
"""


@event('001')
@rule('.*')
@sopel.module.thread(True)
def bot_startup_dict_coms(bot, trigger):

    # don't run jobs if not ready
    while not bot_startup_requirements_met(bot, ["botdict", "modules", "dict_coms"]):
        pass

    bot.memory["botdict"]["tempvals"]['all_coms'] = []

    bot.memory["botdict"]["tempvals"]['all_coms'].extend(bot.memory["botdict"]["tempvals"]['dict_commands'].keys())

    bot.memory["botdict"]["tempvals"]['all_coms'].extend(bot.memory["botdict"]["tempvals"]['module_commands'].keys())

    bot_startup_requirements_set(bot, "all_coms")
