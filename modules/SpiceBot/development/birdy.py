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


@sopel.module.commands('birdy')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    rand = random.randint(1,2)
    if rand == 1:
        osd(bot, trigger.sender, 'say', "________________$$$$_________________")
        osd(bot, trigger.sender, 'say', "______________$$____$$_______________")
        osd(bot, trigger.sender, 'say', "______________$$____$$_______________")
        osd(bot, trigger.sender, 'say', "______________$$____$$_______________")
        osd(bot, trigger.sender, 'say', "______________$$____$$_______________")
        osd(bot, trigger.sender, 'say', "______________$$____$$_______________")
        osd(bot, trigger.sender, 'say', "__________$$$$$$____$$$$$$___________")
        osd(bot, trigger.sender, 'say', "________$$____$$____$$____$$$$_______")
        osd(bot, trigger.sender, 'say', "________$$____$$____$$____$$__$$_____")
        osd(bot, trigger.sender, 'say', "$$$$$$__$$____$$____$$____$$____$$___")
        osd(bot, trigger.sender, 'say', "$$______$$______________________$$___")
        osd(bot, trigger.sender, 'say', "$$____$$$$________________$$____$$___")
        osd(bot, trigger.sender, 'say', "__$$____$$______________________$$___")
        osd(bot, trigger.sender, 'say', "___$$$__$$______________________$$___")
        osd(bot, trigger.sender, 'say', "____$$__________________________$$___")
        osd(bot, trigger.sender, 'say', "_____$$$________________________$$___")
        osd(bot, trigger.sender, 'say', "______$$______________________$$$____")
        osd(bot, trigger.sender, 'say', "_______$$$____________________$$_____")
        osd(bot, trigger.sender, 'say', "________$$____________________$$_____")
        osd(bot, trigger.sender, 'say', "_________$$$________________$$$______")
        osd(bot, trigger.sender, 'say', "__________$$________________$$_______")
        osd(bot, trigger.sender, 'say', "__________$$$$$$$$$$$$$$$$$$$$_______")
    else:
        target = get_trigger_arg(bot, triggerargsarray, 1)
        if not target:
            test
        osd(bot, trigger.sender, 'say', "do the thing")
