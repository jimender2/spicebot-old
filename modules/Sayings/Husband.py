#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import random
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

replies = ["Honey, how do I change a diaper?", "If you put it on the to-do list, I told you I'll do it. You don't have to remind me about it every 6 months.", "*Buuuurp*", "Sure honey, that's fine.", "*Sigh* Yes dear."]
actions = ["burps", "scratches his ass", "farts", "opens a beer"]

@sopel.module.commands('husband')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    decide = random.randint(1,10)
    if decide > 7:
        response = get_trigger_arg(bot, actions, 'random')
        bot.action(response)
    else:	
        answer = get_trigger_arg(bot, replies, 'random')
        bot.say(answer)
	
