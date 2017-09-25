import sopel.module
import requests
import json

@sopel.module.rate(120)
@sopel.module.commands('isitaholiday')
def isitaholiday(bot,trigger):
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
