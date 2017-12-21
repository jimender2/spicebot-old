#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import random
import sys
import os
import requests
import urllib2
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('google','googleit')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    searchterm = get_trigger_arg(triggerargsarray, 0)
    if not searchterm:
        bot.say('Please enter a term to search for')
    else:
        data = searchterm.strip().lower()
        data=data.replace(' ', '%20').replace('site:', 'site%3A')
        var = requests.get(r'http://www.google.com/search?q=' + data + '&btnI')
        bot.say(str(var.url))
    
