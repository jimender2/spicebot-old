#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('wah')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    target = get_trigger_arg(bot, triggerargsarray, 1)
    validtarget=targetcheck(bot,get_trigger_arg(bot, triggerargsarray, 1),trigger.nick)
    if validtarget == 1:
        bot.say(trigger.nick + " calls the waaaaaaaaaaahhhhhhmbulance for " + target)
    elif validtarget==2 or validtarget==3:
        bot.action("calls the waaaaaaaaaaahhhhhhmbulance for " + trigger.nick)    
    else:
        bot.say(trigger.nick + " calls the waaaaaaaaaaahhhhhhmbulance.")
