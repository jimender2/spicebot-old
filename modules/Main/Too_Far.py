#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('toofar')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    item = get_trigger_arg(triggerargsarray, 0)
    if not item:
        bot.say("What can you risk going too far?")
    else:
        if not item.endswith('ing'):
            itema = str(item + "ing")
            itemb = item
        else:
            itema = item
            itemb = item.replace('ing','')
        bot.say("Only those people who risk " + str(itema) + " too far, ever find out how far they can " + str(itemb) + "!")
