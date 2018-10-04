#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
import random
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# contributer jimender2


@sopel.module.commands('warn')
def mainfunction(bot, trigger):
    inchannel = trigger.sender
    triggerargsarray = spicemanip(bot, trigger.group(2), 'create')
    target = spicemanip(bot, triggerargsarray, 2) or ''
    rand = random.randint(1, 10)
    if rand < 5:
        osd(bot, inchannel, 'say', target + "This is just a warning. Overuse of the bot can get you kicked or banned by an operator. If you want to purely play with the bot, go to #Spicebottest, or send Spicebot a PrivateMessage.")
    else:
        osd(bot, inchannel, 'say', target + "This is just a warning. Underuse of the bot can get you kicked or banned by an operator. If you want to not play with the bot, go to Canada or some other place that no one cares about.")
