#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('wanted')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    target = get_trigger_arg(triggerargsarray, 1)
    validtarget,validmsg=checktarget(bot,trigger.nick,get_trigger_arg(triggerargsarray, 1)
    if validtarget == 1:
      bot.say(trigger.nick + " calls the waaaaaaaaaaahhhhhhmbulance for " + target)
    elif validtarget==2:
      bot(trigger.nick + " calls the waaaaaaaaaaahhhhhhmbulance to take them away.")
    else:
      bot.say(trigger.nick + " calls the waaaaaaaaaaahhhhhhmbulance.")
