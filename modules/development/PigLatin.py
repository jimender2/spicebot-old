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

@sopel.module.commands('piglatin','pl')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'piglatin')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)

def execute_main(bot, trigger, triggerargsarray):
    instigator = trigger.nick
    words = get_trigger_arg(bot, triggerargsarray, '1+')
    
    pyg = 'ay'

    if len(words) > 0:
        words = words.lower()
        first = words[0]
        if first == ('a' or 'e' or 'i' or 'o' or 'u'):
            new_word = word + pyg
            bot.say(new_word)
        else:
            new_word = word[1:] + first + pyg
            bot.say(new_word)
    else:
        bot.say("Oink oink")
