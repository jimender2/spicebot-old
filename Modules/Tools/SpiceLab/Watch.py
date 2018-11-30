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


# Start listener on welcome RPL, which should only ever be received once
@event('002')
@rule('.*')
@sopel.module.thread(True)
def watch_events_test(bot, trigger):

    while 'botdict_loaded' not in bot.memory:
        time.sleep(1)

    for value in ["trigger", "trigger.args", "trigger.line", "trigger.event", "trigger.tags", "trigger.nick", "trigger.sender", "trigger.hostmask", "trigger.user", "trigger.time", "trigger.is_privmsg", "trigger.admin", "trigger.owner"]:
        try:
            valueeval = str(eval(value))
            valueeval = str(value + " = " + valueeval)
        except Exception as e:
            valueeval = str("error with " + str(value))
        bot.msg("#spicebottest", str(valueeval))
