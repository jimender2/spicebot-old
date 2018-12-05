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

# author dysonparkes


@sopel.module.commands('test')
def mainfunction(bot, trigger):
    """Check to see if module is enabled."""

    execute_main(bot, trigger)


def execute_main(bot, trigger):
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
