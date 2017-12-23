#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
from sopel.module import commands, example, NOLIMIT
import random
import sys
import os
import requests
import urllib2
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

def searchfor(data):
    data=data.replace(' ', '%20')
    var = requests.get(r'http://www.google.com/search?q=' + data + '&btnI')
    query=str(var.url)
    return query

@commands('google')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    triggerargsarray = create_args_array(trigger.group(2)) ## triggerarg 0 = commandused
    searchterm = get_trigger_arg(triggerargsarray, 1)
    query=''
    if not searchterm:
        bot.say('Please enter a term to search for')        
    else:
        data = searchterm.strip().lower()
        data=data.replace('site:', 'site%3A')
        query=searchfor(data)
        if not query:
            bot.say('I cannot find anything about that')
        else:
            bot.say(query)
            
@commands('youtube')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    triggerargsarray = create_args_array(trigger.group(2)) ## triggerarg 0 = commandused    
    searchterm = get_trigger_arg(triggerargsarray, 1)
    query=''
    data = searchterm.strip().lower()
    data+='site%3Ayoutube.com'
    query=searchfor(data)
    if not query:
        bot.say('I cannot find anything about that')
    else:
        bot.say(query)
            

    
