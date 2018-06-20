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
    words = get_trigger_arg(bot, words, 'create')
    
    pyg = 'ay'
    firstsarray = ['a','e','i','o','u']

    rebuildarray = []
    if len(words) > 0:
        for word in words:
            word = word.lower()
            first = word[0]
            bot.say(str(first))
            if first in firstsarray:
                new_word = word + pyg
            else:
                new_word = word[1:] + first + pyg
            rebuildarray.append(new_word)
        words = get_trigger_arg(bot, words, 0)
        bot.say(words)
    else:
        bot.say("Oink oink")
