import sopel.module
import requests
import json
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('wouldyourather','wyr')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    joke = getJoke(trigger.group(2).strip())
    if joke:
        bot.say(joke)
    else:
        bot.say('I would rather not give you a response.')

def getJoke(trigger):
    if trigger='nsfw':
        url = 'http://www.rrrather.com/botapi?nsfw=true'
    else:
        url = 'http://www.rrrather.com/botapi'
    try:
      page = requests.get(url)
      result = page.content
      jsonjoke = json.loads(result)
      joke = jsonjoke['title'] + " A:" + jsonjoke['choicea'] + " or B:" + jsonjoke['choiceb']
    except:
      joke = "I would rather not."
    return joke
