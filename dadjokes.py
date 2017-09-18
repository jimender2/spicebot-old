import sopel.module
import aiohttp

@sopel.module.commands('dad','dadjoke')
def sayDadJoke(bot,trigger):
    joke = getDadJoke()
    if joke:
        bot.say(joke)
    else:
        bot.say('My humor module is broken.')
        

def getDadJoke():
    url = 'https://icanhazdadjoke.com'
    r = aiohttp.request('GET', url, header = {'Accept:': 'text/plain'}) 
    joke = r.text()
    return joke
