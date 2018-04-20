#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
from SpicebotShared import *
import sopel.module
import sys
import os
import urllib2
import json
import random

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
    type,question,arrAnswers,answer = getQuestion()
    if type == "boolean":
        question = "True or False: " + question
    bot.say("Question: " + question)
    bot.say("Choices: A)" + arrAnswers[0] + " B)" + arrAnswers[1] + " C)" + arrAnswers[2] + " D)" + arrAnswers[3])
    bot.say("Answer: " + answer)
    

def getQuestion():
    url = 'https://opentdb.com/api.php?amount=1'
    data = json.loads(urllib2.urlopen(url).read())
    
    wrongAnswers = data['results'][0]
    wrongAnswers = wrongAnswers['incorrect_answers']
    arrWrong = str(wrongAnswers).split("',")
    choiceOne = arrWrong[0].replace("u'","",1).strip()
    choiceTwo = arrWrong[1].replace("u'","",1).strip()
    choiceThree = arrWrong[2].replace("u'","",1).strip()
    
    results = str(data['results'])
    a = results.split("',") 
    type = splitEntry(a[1])
    question  = splitEntry(a[2])
    answer = splitEntry(a[4])
    
    choiceOne = sanitizeString(choiceOne)
    choiceTwo = sanitizeString(choiceTwo)
    choiceThree = sanitizeString(choiceThree)
    answer = sanitizeString(answer)
    arrAnswers = [choiceOne,choiceTwo,choiceThree,answer]
    random.shuffle(arrAnswers)
    
    return type,question,arrAnswers,answer

def splitEntry(entry):
    splitChar = ':'
    a = entry.split(splitChar)
    result = a[1]
    result = result.replace("u'","",1).strip()
    result = sanitizeString(result)
    return result

def sanitizeString(entry):
    result = entry.replace('[','')
    result = result.replace(']','')
    result = result.replace("&quot;",'"')
    result = result.replace("&#039","'")
    return result
    
    
