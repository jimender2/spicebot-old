import sopel.module
import requests
import json
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('urmom')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    joke = getJoke()
    target = get_trigger_arg(triggerargsarray, 1)
    for c in bot.channels:
        channel = c
    if joke:
        if not target:
            bot.say(joke)
        else:
            if not target.lower() not in bot.privileges[channel.lower()]:
                if target == bot.nick:        
                    bot.say('I have no mother' )            
                else:
                    bot.say('Hey, ' + target + '! ' + joke) 
    else:
        bot.say('Please leave the mothers out of it.')

def getJoke():
    url = 'http://api.yomomma.info'
    try:
      page = requests.get(url)
      result = page.content
      jsonjoke = json.loads(result)
      joke = jsonjoke['joke']
    except:
      joke = "yo momma broke the interwebs."
    return joke
