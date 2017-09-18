import sopel.module
import requests
from fake_useragent import UserAgent

@sopel.module.commands('dad','dadjoke')
def sayDadJoke(bot,trigger):
    joke = getDadJoke()
    if joke:
        bot.say(joke)
    else:
        bot.say('My humor module is broken.')
        

def getDadJoke():
    url = 'https://icanhazdadjoke.com'
    'ua = UserAgent()
    page = requests.get(url,headers = {'Accept':'text/plain'})
    joke = page.content
    return joke
