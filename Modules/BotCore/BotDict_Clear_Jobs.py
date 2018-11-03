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


@sopel.module.interval(60)  # 5 mins is 300
def run_saved_jobs(bot):

    # don't run jobs if not ready
    if "botdict_loaded" not in bot.memory:
        return

    bot_saved_jobs_run(bot)


def bot_saved_jobs_process(bot, trigger, jobtype):
    dictsave = {"jobtype": jobtype, "bot": bot, "trigger": trigger}

    bot_saved_jobs_save(bot, dictsave)


def bot_saved_jobs_save(bot, dictsave):

    if "bot_jobs" not in bot.memory:
        bot.memory["bot_jobs"] = []

    bot.memory["bot_jobs"].append(dictsave)


def bot_saved_jobs_run(bot):

    if "bot_jobs" not in bot.memory:
        bot.memory["bot_jobs"] = []

    for botjob_dict in bot.memory["bot_jobs"]:
        bot.msg("#spicebottest", str(botjob_dict))

    # Clear them out
    bot.memory["bot_jobs"] = []
