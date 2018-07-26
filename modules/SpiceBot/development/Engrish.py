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

# author jimender2


@sopel.module.commands('engrish')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'engrish')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    message = get_trigger_arg(bot, triggerargsarray, '1+')
    message = message.replace('r', 't', 1)
    message = message.replace('l', 'b', 3)
    message = message.replace('a', 'l', 6)
    message = message.replace('e', 'f', 4)
    message = message.replace('y', 'c', 2)
    message = message.replace('t', 'n', 4)
    message = message.replace('z', 'a', 9)
    message = message.replace('p', 'e', 7)
    message = message.replace('q', 'p')
    osd(bot, trigger.sender, 'say', message)
