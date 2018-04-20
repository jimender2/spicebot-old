#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
from SpicebotShared import *
import sopel.module
import sys
import os
import urllib2
import json

moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)

@sopel.module.commands('trivia')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)

def execute_main(bot, trigger, triggerargsarray):
    question,answer = getQuestion()
    bot.say("Question: " + question)
    bot.say("Answer: " + answer)
    

def getQuestion():
    url = 'https://opentdb.com/api.php?amount=1'
    data = json.loads(urllib2.urlopen(url).read())
    results = str(data['results'])
    a = results.split("',")    
    question  = splitEntry(a[2])
    answer = splitEntry(a[4])
    return question,answer

def splitEntry(entry):
    splitChar = ':'
    a = entry.split(splitChar)
    result = a[1]
    result = result.replace("u'","'",1)
    return result
