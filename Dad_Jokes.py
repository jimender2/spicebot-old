import sopel.module
import requests

@sopel.module.rate(120)
@sopel.module.commands('dad','dadjoke')
def sayDadJoke(bot,trigger):
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
