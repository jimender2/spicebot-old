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
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@commands('google', 'search')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'google')
    if not enablestatus:
        execute_main(bot, trigger, args, triggerargsarray)
    
def execute_main(bot, trigger, args, triggerargsarray):
    if len(args)>=1:
        mysite = args[0].lower()
        searchterm = get_trigger_arg(triggerargsarray, '1+')
        querystring = get_trigger_arg(triggerargsarray, '2+')
        if (mysite == 'video' or mysite == 'youtube'):           
            data=querystring.replace(' ', '+')
            site = '+site%3Ayoutube.com'
            url = 'https://www.youtube.com/'
            url2 = 'https://youtube.com/'
            searchterm = data+site
            query=searchfor(searchterm)
            if not query:
                bot.say('I cannot find anything about that')
            else:
                if(str(query).startswith(url) or str(query).startswith(url2)):
                    bot.say(query)
                else:
                    bot.say(query)
                    bot.say('Valid website not found')

        elif mysite == 'meme':
            data=querystring.replace(' ', '+') 
            site = '+site%3Aknowyourmeme.com'
            url = 'knowyourmeme.com'
            searchterm = data+site
            query=searchfor(searchterm)
            if not query:
                bot.say('I cannot find anything about that')
            else:
                if str(query).startswith(url):
                    bot.say(query)
                else:
                    bot.say('I could not find that but check this out: https://www.youtube.com/watch?v=dQw4w9WgXcQ')

        elif mysite == 'walmart':
            data=querystring.replace(' ', '+') 
            site = '+site%3Apeopleofwalmart.com'
            url = 'http://www.peopleofwalmart.com'
            searchterm = data+site
            query=searchfor(searchterm)
            if not query:
                bot.say('https://goo.gl/SsAhv')
            else:
                if str(query).startswith(url):
                    bot.say(query)
                else:
                    bot.say('I could not find that but check this out: https://www.youtube.com/watch?v=dQw4w9WgXcQ')                       

        else:
            data=searchterm.replace(' ', '+')
            query=searchfor(data)
            if not query:
                bot.say('I cannot find anything about that')
            else:
                bot.say(query)   
     

def searchfor(data):
    var = requests.get(r'http://www.google.com/search?q=' + data + '&btnI')
    query=str(var.url)
    return query            

    
