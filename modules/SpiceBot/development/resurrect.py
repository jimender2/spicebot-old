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

# author jimender2


@sopel.module.commands('resurrect')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    instigator = trigger.nick
    target = spicemanip(bot, triggerargsarray, 1)
    targetcheck = easytargetcheck(bot, botcom, target, instigator)

    if targetcheck == "instigator":
        osd(bot, trigger.sender, 'say', "You are not able to resurrect yourself dumbass")
    elif targetcheck == "bot":
        osd(bot, trigger.sender, 'say', "I hope you relize that I am immortal (and immoral)")
    elif targetcheck == "false":
        osd(bot, trigger.sender, 'say', "You do relize that " + target + " is not a person so quit pretending you have friend's")
    elif targetcheck == "offline":
        osd(bot, trigger.sender, 'say', "I dont see " + target + ". Where did they go?")
    elif targetcheck == "online":
        rand = random.randomint(1,4)
        osd(bot, trigger.sender, 'say', instigator + " wants to know if " + target + "'s carpets matches the drapes")
    else:
        osd(bot, trigger.sender, 'say', "You do relize that " + target + " is not a person so quit pretending you have friend's")