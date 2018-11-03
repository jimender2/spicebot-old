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
sys.setrecursionlimit(4096)


@sopel.module.interval(60)  # 5 mins is 300
def run_saved_jobs(bot):

    # don't run jobs if not ready
    if "botdict_loaded" not in bot.memory:
        return

    bot_saved_jobs_run(bot)
