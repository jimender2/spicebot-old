#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('sign', 'politics', 'religion', 'genders')
def execute_main(bot, trigger):
    channel = trigger.sender
    osd(bot, trigger.sender, 'say', "NO POLITICS, RELIGION, OR EXCESSIVE GENDER/SJWing IN " + channel + "!")
