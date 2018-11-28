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


@sopel.module.commands('devtest')
@sopel.module.thread(True)
def seen(bot, trigger):

    # bot.msg("#spicebottest", str(bot.privileges))
    for botname in bot.privileges.keys():
        bot.msg("#spicebottest", str(botname))
