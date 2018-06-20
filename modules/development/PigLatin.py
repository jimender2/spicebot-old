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
    wordsToConvert = get_trigger_arg(bot, triggerargsarray, '1+')
    
    numberOfWords = len(wordsToConvert)
    
    i = 1
    while (numberOfWords >= i):
        workingWord = wordsToConvert[i]
        letters = len(workingWord)
        d = letters - 1
        working = workingWord(d)
        message = message + working + " "
    
    bot.say(message)
