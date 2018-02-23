#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
from sopel.module import commands, example, NOLIMIT
import random
import sys
import os
import requests
import re
import urllib2
import sopel.web as web
import json
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@commands('urban')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'google')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
        
def execute_main(bot, trigger, triggerargsarray):
    if len(triggerargsarray)>=1:
        mysite = get_trigger_arg(bot, triggerargsarray, 1).lower()
        searchterm = get_trigger_arg(bot, triggerargsarray, '1+')
        querystring = get_trigger_arg(bot, triggerargsarray, '2+')
    word = trigger.group(2)
    if not word:
        return bot.say(urbandict.__doc__.strip())

    try:
        data = web.get("http://api.urbandictionary.com/v0/define?term={0}".format(web.quote(word)))
        data = json.loads(data)
    except:
        return bot.say("Error connecting to urban dictionary")
        
    if data['result_type'] == 'no_results':
        return bot.say("No results found for {0}".format(word))

    result = data['list'][0]
    url = 'http://www.urbandictionary.com/define.php?term={0}'.format(
        web.quote(word))

    response = "{0} - {1}".format(result['definition'].strip()[:256], url)
    bot.say(response)

#if __name__ == '__main__':
    #print(__doc__.strip())
