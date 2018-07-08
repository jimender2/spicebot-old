#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import urllib2
import json
from BeautifulSoup import BeautifulSoup
from random import randint
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

#author jimender2

@sopel.module.commands('tmyk', 'themoreyouknow')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    gif = magicFingers()
    if gif:
        bot.say(gif)
    else:
        bot.action('the more you know... **magic fingers**')
        
def magicFingers():
    api = 'Wi33J3WxSDxWsrxLREcQqmO3iJ0dk52N'
    url = 'http://api.giphy.com/v1/gifs/search?q=themoreyouknow&api_key=' + api + '&limit=50'
    data = json.loads(urllib2.urlopen(url).read())
    randno = randint(1,49)
    id = data['data'][randno]['id']
    gif = 'https://media2.giphy.com/media/'+id+'/giphy.gif'
    return gif