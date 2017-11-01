import sopel.module
import requests
import json
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.rate(120)
@sopel.module.commands('urmom')
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
                bot.say('Hey, ' + trigger.group(2).strip() + '! ' + joke)        
        else:
            bot.say('Please leave the mothers out of it.')
