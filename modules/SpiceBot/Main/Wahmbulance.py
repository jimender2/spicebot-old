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

@sopel.module.commands('wah')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)

def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    target = get_trigger_arg(bot, triggerargsarray, 1)
    validtarget=targetcheck(bot,get_trigger_arg(bot, triggerargsarray, 1),trigger.nick)
    if validtarget == 1:
        osd(bot, trigger.sender, 'say', trigger.nick + " calls the waaaaaaaaaaahhhhhhmbulance for " + target)
    elif validtarget==2 or validtarget==3:
        bot.action("calls the waaaaaaaaaaahhhhhhmbulance for " + trigger.nick)
    else:
        osd(bot, trigger.sender, 'say', trigger.nick + " calls the waaaaaaaaaaahhhhhhmbulance.")
