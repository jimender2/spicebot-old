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
    bot.say("\n_________$$____________\n\n"
            "\n________$__$___________\n\n"
            "\n________$__$___________\n\n"
            "\n_______$$__$$__________\n\n"
            "\n______$__$__$_$$_$$____\n\n"
            "\n______$__$__$__$$__$___\n\n"
            "\n_$$$__$__$__$__$$__$___\n\n"
            "\n$___$$_______________$_\n\n"
            "\n$____$$_______________$\n\n"
            "\n_$____________________$\n\n"
            "\n__$___________________$\n\n"
            "\n___$_________________$_\n\n"
            "\n____$_______________$__\n\n"
            "\n_____$_____________$___\n\n"
            "\n______$___________$____\n\n"
            "\n_______$$$$$$$$$$$_____\n\n")
