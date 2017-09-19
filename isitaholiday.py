import sopel.module
import requests
import json

@sopel.module.commands('isitaholiday')
def isitaholiday(bot,trigger):
    holiday = getholiday()
    if holiday == 'false':
        bot.say('Today Is Not A Holiday.')
    else:
        bot.say('The Current Holiday Is: ' + holiday)

def getholiday():
    url = 'http://isitaholiday.herokuapp.com/api/v2/holidays/today/'
    page = requests.get(url)
    result = page.content
    jsonholiday = json.loads(result)
    holiday = jsonholiday['status']
    return holiday
