#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import requests
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

@sopel.module.commands('dad','dadjoke')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'dad')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)

def execute_main(bot, trigger, triggerargsarray):
    joke = getDadJoke()
    if joke:
        bot.say(joke)
    else:
        bot.say('My humor module is broken.')

def getDadJoke():
    url = 'https://icanhazdadjoke.com'
    page = requests.get(url,headers = {'Accept':'text/plain'})
    joke = page.content
    return joke
