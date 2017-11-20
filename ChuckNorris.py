import sopel.module
import requests
import json
import sys
import os
import html2text
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('chucknorris','chuck')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    joke = getJoke()
    if joke:
        if not trigger.group(2):
            bot.say(joke)
        elif not trigger.group(2).strip() == bot.nick:
            joke = joke.replace('Chuck Norris', trigger.group(2).strip())
            joke = joke.replace('chuck norris', trigger.group(2).strip())
            joke = joke.replace('Norris', trigger.group(2).strip())
            joke = joke.replace('Chuck', trigger.group(2).strip())
            bot.say(joke)        
    else:
        bot.say('Chuck will find you.')

def getJoke():
    url = 'http://api.icndb.com/jokes/random'
    try:
      page = requests.get(url)
      result = page.content
      jsonjoke = json.loads(result)
      #joke = html2text.html2text(jsonjoke['value']['joke'])
      joke = jsonjoke['value']['joke']
    except:
      joke = "Chuck Norris broke the interwebs."
    return joke
