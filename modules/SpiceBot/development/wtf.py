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

randomWordArray = ["flying fuck", "frickle frackal", "fuck", "fudgical", ""]


@sopel.module.commands('wtf', 'whatthefuck')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'wtf')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    instigator = trigger.nick
    rand = random.randint(1,5)
    target = get_trigger_arg(bot, triggerargsarray, 1)
    check = easytargetcheck(bot, botcom, target, instigator)
    if check == 'bot':
        message = "What the fuck " + bot.nick
    elif check == 'instigator':
        message = "What the fuck "
    elif check == 'valid':
        message = "What the fuck " + target

    osd(bot, trigger.sender, 'say', "do the thing")
