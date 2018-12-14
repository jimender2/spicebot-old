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
@sopel.module.url('(.*)')
@sopel.module.url('https?://twitter.com/([^/]*)(?:/status/(\d+)).*')
@sopel.module.url(r'xkcd.com/(\d+)')
"""


@sopel.module.url(r'xkcd.com/(\d+)')
@sopel.module.thread(True)
def bot_url_hub(bot, trigger):

    # don't run jobs if not ready
    while not bot_startup_requirements_met(bot, ["connected", "botdict", "server", "channels", "users"]):
        pass

    bot.msg("#spicebottest", str(trigger))
    bot.msg("#spicebottest", str(trigger.args))
