#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('sign','politics','religion','genders')
def execute_main(bot, trigger):
    channel = trigger.sender
    bot.say("NO POLITICS, RELIGION, OR EXCESSIVE GENDER/SJWing IN " + channel + "!")
