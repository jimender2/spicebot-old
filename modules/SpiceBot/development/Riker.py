#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import random
import urllib
import urllib2
import sys
import os
from word2number import w2n
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

site = 'https://raw.githubusercontent.com/deathbybandaid/SpiceBot/master/Text-Files/riker.txt'


@sopel.module.commands('riker')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    data = urllib.urlopen(site).read()
    data = data.split(" ")
    max = int(get_trigger_arg(bot, triggerargsarray, 1))
    max = max
    message = ""

    i = 0
    while i <= max:
        meassage = message + data[i]
        i++

    osd(bot, trigger.sender, 'say', message)
