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
    rand = random.randint(1, 2)
    if rand == 1:
<<<<<<< HEAD
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
=======
        bot.say("_________$$____________'\n'________$__$___________'\n'________$__$___________'\n'_______$$__$$__________'\n'______$__$__$_$$_$$____'\n'______$__$__$__$$__$___'\
                 '_$$$__$__$__$__$$__$___'\
                 '$___$$_______________$_'\
                 '$____$$_______________$'\
                 '_$____________________$'\
                 '__$___________________$'\
                 '___$_________________$_'\
                 '____$_______________$__'\
                 '_____$_____________$___'\
                 '______$___________$____'\
                 '_______$$$$$$$$$$$_____")
>>>>>>> 41c94ad981db391be22ca743ce1b60025bb15fd7
    else:
        target = get_trigger_arg(bot, triggerargsarray, 1)
        instigator = trigger.nick
        if not target:
            message = instigator + " shows the birdy off to everyone in the room"
        osd(bot, trigger.sender, 'say', "Your shit is broken")
