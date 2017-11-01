import sopel.module
import requests
import json
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.rate(120)
@sopel.module.commands('isitaholiday')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    holiday = getholiday()
    if holiday:
        bot.say('Today is a holiday.')
    else:
        bot.say('Today is not a holiday.')

def getholiday():
    url = 'http://isitaholiday.herokuapp.com/api/v2/holidays/today/'
    page = requests.get(url)
    result = page.content
    jsonholiday = json.loads(result)
    holiday = jsonholiday['status']
    return holiday
