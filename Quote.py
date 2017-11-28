import sopel.module
import requests
import json
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('quote')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    quote = getQuote()
    if quote:
        bot.say(quote)
    else:
        bot.say('There is nothing to quote - Abraham Lincoln')

def getQuote():
    url = 'http://quotesondesign.com/wp-json/posts?filter[orderby]=rand&filter[posts_per_page]=1'
    try:
      page = requests.get(url)
      result = page.content
      jsonquote = json.loads(result)
      quote = '"' + jsonquote['content'] + '" - ' + jsonquote['title']
    except:
      quote = "No quote for you."
    return quote
