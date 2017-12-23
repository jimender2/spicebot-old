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

@sopel.module.commands('video','google','googleit','search','youtube')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    triggerargsarray = create_args_array(trigger.group(2)) ## triggerarg 0 = commandused
    commandused = trigger.group(1) 
    searchterm = get_trigger_arg(triggerargsarray, 1)
    query=''
    if not searchterm:
        bot.say('Please enter a term to search for')
    else:
        if (commandused=='video' or commandused=='youtube'):
            data = searchterm.strip().lower()
            data+='site%3Ayoutube.com'
            query=searchfor(data)
        else:
            data = searchterm.strip().lower()
            data=data .replace('site:', 'site%3A')
            query=searchfor(data)
        if not query:
            bot.say('I cannot find anything about that')
        else:
            bot.say(query)
            
def searchfor(data):
    data=data.replace(' ', '%20')
    var = requests.get(r'http://www.google.com/search?q=' + data + '&btnI')
    query=str(var.url)
    return query
    
