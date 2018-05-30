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

@sopel.module.commands('random')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    pictype = get_trigger_arg(bot, triggerargsarray, 1)
    outputtext = ''
    if pictype == 'dog':
        outputtext = getoutputtext(bot, 'dog')
    elif pictype == 'cat':
        outputtext = getoutputtext(bot, 'cat')
    else:
        outputtext = str("I don't currently have an api for " + str(pictype))
    if not outputtext:
        outputtext = "An error has occured."
    bot.say(outputtext)

def getoutputtext(bot, pictype):
    if pictype == 'dog':
        url = 'https://random.dog/woof.json'
        jsontype = 'url'
    elif pictype == 'cat':
        url = 'http://aws.random.cat/meow'
        jsontype = 'file'
    try:
      page = requests.get(url)
      result = page.content
      jsonpoop = json.loads(result)
      outputtext = jsonpoop[jsontype]
      #outputtext = outputtext.replace("/","")
    except:
      outputtext = ""
    return outputtext
