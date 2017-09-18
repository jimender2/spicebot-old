import sopel.module
import requests
import json

@sopel.module.commands('urmom')
def sayJoke(bot,trigger):
    joke = getJoke()
    if joke:
        bot.say('Hey, ' + trigger.group(2) + '!' + joke)
    else:
        bot.say('Please leave the mothers out of it.')

def getJoke():
    url = 'http://api.yomomma.info'
    page = requests.get(url,headers = {'Accept':'text/plain'})
    result = page.content
    jsonjoke = json.loads(result)
    joke = jsonjoke['joke']
