#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
from random import randint
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# author = dysonparkes


@sopel.module.commands('fb', 'fuckbucket')
def mainfunction(bot, trigger):
    """Check to see if module is enabled."""
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'fb')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    """Handle the fuckbucket responses."""
    diceroll = randint(0, 6)
    instigator = trigger.nick
    target = spicemanip(bot, triggerargsarray, 1)
    if diceroll <= 2:
        osd(bot, trigger.sender, 'action', "checks the fuckbucket, finds no fucks to give.")
    elif target:
        osd(bot, trigger.sender, 'say', "You know what, %s? I don't think %s has any fucks in their fuckbucket to give." % (target, instigator))
    else:
        osd(bot, trigger.sender, 'say', "Let me check my fuckbucket... Oh, look at that - it's empty.")
