#!/usr/bin/env python
# coding=utf-8
"""Define imports."""
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
import random
import time
from number2words import Number2Words
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# author dysonparkes


@sopel.module.commands('test')
def mainfunction(bot, trigger):
    """Check to see if module is enabled."""
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'test')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    """Run requested command with all possible triggers."""
    commandtotest = spicemanip(bot, triggerargsarray, 1)  # This is the module being tested, entered in chat.
    randomnumber = random.randint(1, 27)
    # The things used to test.
    instigator = trigger.nick
    channel = trigger.sender
    command = "." + commandtotest
    randombot = "SpiceBotdevold"
    randomnumberstring = str(randomnumber)
    randomnumberword = Number2Words(randomnumber).convert()
    blank = ""

    # List of strings to test with.
    args = [instigator, channel, randombot, randomnumberstring, randomnumberword, blank]
    if not commandtotest:
        # Handle if nothing was entered to test.
        osd(bot, trigger.sender, 'say', "What command did you want me to test, " + instigator + "?")
    else:
        # Use the entered command to build strings to test with, and test.
        for arg in args:
            # Use each arg in the list of args individually.
            message = command + " " + arg
            osd(bot, trigger.sender, 'say', message)
            time.sleep(0.250)  # Wait for 100 milliseconds
