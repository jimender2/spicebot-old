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
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *

# Ensure Encoding
reload(sys)
sys.setdefaultencoding('utf-8')


"""
This runs at startup to mark time of bootup
"""


@event('001')
@rule('.*')
@sopel.module.thread(True)
def bot_startup_botinf(bot, trigger):

    # don't run jobs if not ready
    while not bot_startup_requirements_met(bot, ["botdict", "bot_info"]):
        pass

    bot.memory["botdict"]["tempvals"]['txt_files'] = dict()

    # iterate over files within
    for txtfile in os.listdir(bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]["txt_dir"]):

        if txtfile != "ReadMe.MD":

            text_file_list = []
            text_file = open(os.path.join(bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]["txt_dir"], txtfile), 'r')
            lines = text_file.readlines()
            for line in lines:
                text_file_list.append(line)
            text_file.close()

            bot.memory["botdict"]["tempvals"]['txt_files'][txtfile] = text_file_list

    bot_startup_requirements_set(bot, "txt_files")
