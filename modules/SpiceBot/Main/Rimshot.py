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

@sopel.module.commands('rimshot')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)

def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    #bot.action('uses drumsticks to hit both the head and the rim of the drum, then the cymbal.')
    osd(bot, trigger.sender, 'say', '*Ba Dum Tss!!!*')
