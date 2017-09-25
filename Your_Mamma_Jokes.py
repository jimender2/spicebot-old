import sopel.module
import requests
import json

@sopel.module.rate(120)
@sopel.module.commands('urmom')
def sayJoke(bot,trigger):
    joke = getJoke()
    if joke:
        if not trigger.group(2):
            bot.say(joke)
        elif not trigger.group(2) == bot.nick:
            bot.say('Hey, ' + trigger.group(2).strip() + '! ' + joke)        
    else:
        bot.say('Please leave the mothers out of it.')
    

def getJoke():
    url = 'http://api.yomomma.info'
    page = requests.get(url)
    result = page.content
    jsonjoke = json.loads(result)
    joke = jsonjoke['joke']
    return joke
