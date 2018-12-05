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
This counts the python modules
"""


@event('001')
@rule('.*')
@sopel.module.thread(True)
def bot_startup_modules(bot, trigger):

    # don't run jobs if not ready
    while not bot_startup_requirements_met(bot, ["botdict"]):
        pass

    modulecount = 0
    bot.memory["botdict"]["tempvals"]['module_commands'] = dict()
    for modules in bot.command_groups.items():
        filename = modules[0]
        if filename not in ["coretasks"]:
            modulecount += 1
            validcoms = modules[1]
            for com in validcoms:
                bot.memory["botdict"]["tempvals"]['module_commands'][com] = dict()
    bot.memory["botdict"]["tempvals"]['module_count'] = modulecount

    for nickcom in valid_botnick_commands.keys():
        bot.memory["botdict"]["tempvals"]['module_commands'][nickcom] = dict()

    bot_startup_requirements_set(bot, "modules")
