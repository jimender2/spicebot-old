#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import requests
import json
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('wouldyourather','wyr','rather')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'wouldyourather')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    joke = getJoke()
    if joke:
        bot.say(joke)
    else:
        bot.say('I would rather not give you a response.')

def getJoke():
    url = 'http://www.rrrather.com/botapi?nsfw=true'
    try:
      page = requests.get(url)
      result = page.content
      jsonjoke = json.loads(result)
      joke = jsonjoke['title'] + " A: " + jsonjoke['choicea'] + " or B: " + jsonjoke['choiceb']
    except:
      joke = "I would rather not."
    return joke
