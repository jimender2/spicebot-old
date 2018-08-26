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
    rand = random.randint(1,2)
    if rand == 1:
        bot.say("_________$$____________" \n
                "________$__$___________" \n
                "________$__$___________" \n
                "_______$$__$$__________" \n
                "______$__$__$_$$_$$____" \n
                "______$__$__$__$$__$___" \n
                "_$$$__$__$__$__$$__$___" \n
                "$___$$_______________$_" \n
                "$____$$_______________$" \n
                "_$____________________$" \n
                "__$___________________$" \n
                "___$_________________$_" \n
                "____$_______________$__" \n
                "_____$_____________$___" \n
                "______$___________$____" \n
                "_______$$$$$$$$$$$_____")
    else:
        target = get_trigger_arg(bot, triggerargsarray, 1)
        instigator = trigger.nick
        if not target:
            message = instigator + " shows the birdy off to everyone in the room"
        osd(bot, trigger.sender, 'say', "Your shit is broken")
