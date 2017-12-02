import sopel.module
import requests
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('dad','dadjoke')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    joke = getDadJoke()
    if joke:
        bot.say(joke)
    else:
        bot.say('My humor module is broken.')

def getDadJoke():
    url = 'https://icanhazdadjoke.com'    
    page = requests.get(url,headers = {'Accept':'text/plain'})
    joke = page.content
    return joke
