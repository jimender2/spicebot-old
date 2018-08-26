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

# author SniperClif


@sopel.module.commands('middle')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    bot.say("\n_________$$____________\n"
            "\n________$__$___________\n"
            "\n________$__$___________\n"
            "\n_______$$__$$__________\n"
            "\n______$__$__$_$$_$$____\n"
            "\n______$__$__$__$$__$___\n"
            "\n_$$$__$__$__$__$$__$___\n"
            "\n$___$$_______________$_\n"
            "\n$____$$_______________$\n"
            "\n_$____________________$\n"
            "\n__$___________________$\n"
            "\n___$_________________$_\n"
            "\n____$_______________$__\n"
            "\n_____$_____________$___\n"
            "\n______$___________$____\n"
            "\n_______$$$$$$$$$$$_____\n")
