#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
import random
from word2number import w2n
from number2words import Number2Words
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# author dysonparkes


@sopel.module.commands('test')
def mainfunction(bot, trigger):
    """Check to see if module is enabled. """
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'test')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    """Run requested command with all possible triggers."""
    commandtotest = spicemanip(bot, triggerargsarray, 1)
    instigator = trigger.nick
    channel = trigger.sender
    command = "." + commandtotest
    randombot = "SpiceBotdevold"
    randomnumber = random.randint(1, 10)
    randomnumberstring = str(randomnumber)
    randomnumberword = Number2Words(randomnumber).convert()
    randomadmin = ""
    blank = ""
    args = [instigator, channel, randombot, randomnumberstring, randomnumberword, blank]
    if not commandtotest:
        osd(bot, trigger.sender, 'say', "What command did you want me to test, " + instigator + "?")
    else:
        for arg in args:
            message = command + " " + arg
            osd(bot, trigger.sender, 'say', message)
