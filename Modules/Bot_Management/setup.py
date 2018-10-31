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


def setup(bot):

    # botcom dynamic Class
    botcom = class_create('botcom')
    botcom.default = 'botcom'

    # Load global dict
    open_botcomdict(bot, botcom)

    # Channel Listing
    botcom_command_channels_setup(bot, botcom)