#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('matrix')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    pill = get_trigger_arg(bot, triggerargsarray, 1)
    if not pill:
        bot.say('You have two choices. redpill or bluepill')      
    elif pill == 'redpill':
        bot.say('You take the red pill, you stay in Wonderland, and I show you how deep the rabbit hole goes.')
    elif pill == 'bluepill':
        bot.say('You take the blue pill, the story ends. You wake up in your bed and believe whatever you want to believe.')
    
