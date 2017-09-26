import sopel.module
import urllib2
import json
from BeautifulSoup import BeautifulSoup
from random import randint


@sopel.module.rate(120)
@sopel.module.commands('thanks','thanksspicebot')

def thanks(bot,trigger):
    gif = yourewelcome()
    if gif:
        bot.say(gif)
    else:
        bot.say('You're welcome!')


def yourewelcome():
    api = 'Wi33J3WxSDxWsrxLREcQqmO3iJ0dk52N'
    url = 'http://api.giphy.com/v1/gifs/search?q=your+welcome&api_key=' + api + '&limit=100'
    data = json.loads(urllib2.urlopen(url).read())
    randno = randint(0,99)
    gif = data['data'][randno]['embed_url']
    return gif
