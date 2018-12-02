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

bot_dict = {}


@event('001')
@rule('.*')
@sopel.module.thread(True)
def bot_startup_botdict_open(bot, trigger):

    # if existing in memory, save, and then close and reopen
    if "botdict" in bot.memory:
        botdict_save(bot)
        del bot.memory["botdict"]

    # open global dict
    global bot_dict
    botdict = bot_dict

    # pull from database and merge, some content is static
    opendict = botdict.copy()
    dbbotdict = get_database_value(bot, bot.nick, 'bot_dict') or dict()
    opendict = merge_botdict(opendict, dbbotdict)
    botdict.update(opendict)

    # done loading
    bot.memory["botdict"] = botdict


# Merge database dict with stock
def merge_botdict(a, b, path=None):
    "merges b into a"
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge_botdict(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                a[key] = b[key]
        else:
            a[key] = b[key]
    return a
