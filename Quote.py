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
    url = 'https://talaikis.com/api/quotes/random/'
    try:
        page = requests.get(url)
        result = page.content
        jsonquote = json.loads(result)
        #quote = '"' + jsonquote['content'] + '" - ' + jsonquote['title']
        quote = '"' + jsonquote['quote'] + '" - ' + jsonquote['quote']
    except:
        quote = "No quote for you."
    return quote
