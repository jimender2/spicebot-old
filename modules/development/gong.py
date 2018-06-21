#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import os
import sys
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

#author jimender2

@sopel.module.commands('gong')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'gong')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
        
def execute_main(bot, trigger, triggerargsarray):
    person = get_trigger_arg(bot,triggerargsarray,1)
    instigator = trigger.nick

    if person == bot.nick:
        message = "Spicebot grabs " + instigator + " with a hook and drags them out of the room."
    else:
        message = "Spicebot grabs " + person + " with a hook and drags them out of the room."
    
    bot.say(message)