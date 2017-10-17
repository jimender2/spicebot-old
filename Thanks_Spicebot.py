import sopel.module
import urllib2
import json
from BeautifulSoup import BeautifulSoup
from random import randint

@sopel.module.rate(120)
@sopel.module.commands('thanks','thanksspicebot')
def thanks(bot,trigger):
    instigator = trigger.nick
    target = trigger.nick
    update_usertotal(bot, target)
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        gif = yourewelcome()
        if gif:
            bot.say(gif)
        else:
            bot.say('You\'re welcome!')
    else:
        instigator = trigger.nick
        warned = bot.db.get_nick_value(target, 'spicebothour_warn') or 0
        if not warned:
            bot.notice(target + ", you have to run .spiceboton to allow her to listen to you.", instigator)
        else:
            bot.notice(target + ", it looks like your access to spicebot has been disabled for a while. Check out ##SpiceBotTest.", instigator)

def update_usertotal(bot, nick):
    usertotal = bot.db.get_nick_value(nick, 'spicebot_usertotal') or 0
    bot.db.set_nick_value(nick, 'spicebot_usertotal', usertotal + 1)

def yourewelcome():
    api = 'Wi33J3WxSDxWsrxLREcQqmO3iJ0dk52N'
    url = 'http://api.giphy.com/v1/gifs/search?q=your+welcome&api_key=' + api + '&limit=100'
    data = json.loads(urllib2.urlopen(url).read())
    randno = randint(0,99)
    id = data['data'][randno]['id']
    gif = 'https://media2.giphy.com/media/'+id+'/giphy.gif'
    return gif

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
