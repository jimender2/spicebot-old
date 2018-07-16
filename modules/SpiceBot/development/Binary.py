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


@sopel.module.commands('binary')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'iao')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    current_translate = get_trigger_arg(bot, triggerargsarray, 0) or 0
    if not current_translate:
        spititout = randint(0, 1)
    else:
        # spititout = map(bin,bytearray(current_translate))
        spititout = ' '.join(format(ord(x), 'b') for x in current_translate)
        # spititout = spititout.replace("[","")
        # spititout = spititout.replace("]","")
        # spititout = spititout.replace("'","")
    onscreentext(bot, ['say'], str(spititout))
