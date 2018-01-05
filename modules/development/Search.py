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
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, args):
    if len(args)==1:
        data=args[0].strip().lower()       
        query=searchfor(data)
        if not query:
            bot.say('I cannot find anything about that')
        else:
            bot.say(query)   
    elif len(args)>=2:
        if not args[1]:
            bot.say('Please choose a type of search you want and what you want to search for')  
        else:
            mysite =args[0].lower()
            data=args[1].lower() 
            bot.say('Data input: ' + data)
            if (mysite == 'video' or mysite == 'youtube'):
                site = '%20site%3Ayoutube.com'
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
                site = 'site%3Aknowyourmeme.com'
                url = 'knowyourmeme.com'
                searchterm = data+site
                query=searchfor(searchterm)
                if not query:
                    bot.say('I cannot find anything about that')
                else:
                    if str(query).startswith(url):
                        bot.say(query)
                    else:
                        bot.say('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
                        
            elif mysite == 'walmart':
                site = 'site%3Apeopleofwalmart.com'
                url = 'http://www.peopleofwalmart.com'
                searchterm = data+site
                query=searchfor(searchterm)
                if not query:
                    bot.say('https://goo.gl/SsAhv')
                else:
                    if str(query).startswith(url):
                        bot.say(query)
                    else:
                        bot.say('https://www.youtube.com/watch?v=dQw4w9WgXcQ')                       
                                            
                        
                     
            else:
                bot.say('Please choose a type of search you want and what you want to search for')
    else:
        bot.say('Please choose a type of search you want and what you want to search for')
             
                  
    
     

def searchfor(data):
    data=data.replace(' ', '%20')
    var = requests.get(r'http://www.google.com/search?q=' + data + '&btnI')
    query=str(var.url)
    return query            

    
