#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
import random
from word2number import w2n
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# author jimender2


@sopel.module.commands('cointoss', 'dieroll')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'coin')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    sides = int( spicemanip(bot, triggerargsarray, 1) )
    if not sides.isdigit():
        try:
            sides = int( w2n.word_to_num(str(sides)))
        except ValueError:
            sides = 2
    rand = random.randint(1, sides)
    if sides > 2:
        msg = trigger.nick + " you rolled a " + rand + " on a " + str(sides) + " sided die."
    else:
        if rand == 1:
            side = "heads"
        elif rand == 2:
            side = "tails"
        else:
            side = "something fucked up"
        msg = trigger.nick + " flipped a coin and got " + str(side) + "."
    osd(bot, trigger.sender, 'say', msg)
