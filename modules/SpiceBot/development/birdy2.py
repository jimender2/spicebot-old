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
        bot.say("_________$$____________\n\n
                 ________$__$___________\n\n
                 ________$__$___________\n\n
                 _______$$__$$__________\n\n
                 ______$__$__$_$$_$$____\n\n
                 ______$__$__$__$$__$___\n\n
                 _$$$__$__$__$__$$__$___\n\n
                 $___$$_______________$_\n\n
                 $____$$_______________$\n\n
                 _$____________________$\n\n
                 __$___________________$\n\n
                 ___$_________________$_\n\n
                 ____$_______________$__\n\n
                 _____$_____________$___\n\n
                 ______$___________$____\n\n
                 _______$$$$$$$$$$$_____")
    else:
        target = get_trigger_arg(bot, triggerargsarray, 1)
        instigator = trigger.nick
        if not target:
            message = instigator + " shows the birdy off to everyone in the room"
        osd(bot, trigger.sender, 'say', "Your shit is broken")
