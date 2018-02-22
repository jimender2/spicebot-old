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

@sopel.module.commands('urmom')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    joke = getJoke()
    target = get_trigger_arg(bot, triggerargsarray, 1)
    for c in bot.channels:
        channel = c
    if joke:
        if not target:
            bot.say(joke)
        else:
            if not target.lower() not in bot.privileges[channel.lower()]:
                if target == bot.nick:        
                    bot.say('I have no mother' )            
                else:
                    bot.say('Hey, ' + target + '! ' + joke)
            else:
                bot.say(target + ' is not here but ' + trigger.nick + ' ' + joke )
    else:
        bot.say('Please leave the mothers out of it.')

def getJoke():
    url = 'http://api.yomomma.info'
    try:
      page = requests.get(url)
      result = page.content
      jsonjoke = json.loads(result)
      joke = jsonjoke['joke']
    except:
      joke = "yo momma broke the interwebs."
    return joke
