import sopel.module
import urllib2
import json
from BeautifulSoup import BeautifulSoup
from random import randint


@sopel.module.rate(120)
@sopel.module.commands('gif','giphy')
def gif(bot,trigger):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        if trigger.nick == 'IT_Sean':
            gif = 'https://media2.giphy.com/media/11aCNnhizTWfXW/giphy.gif'
            bot.say('IT_Sean, you\'re safe with me. ' + gif)
        else:        
            if trigger.group(2):
                query = trigger.group(2).replace(' ', '+')
                gif = getGif(query)
                if gif:
                    bot.say(gif)
                else:
                    bot.say('Hmm...Couldn\'t find a gif for that!')
            else:
                bot.say('Tell me what you\'re looking for!')
    else:
        instigator = trigger.nick
        bot.notice(target + ", you have to run .spiceboton to allow her to listen to you.", instigator)

def getGif(query):
    api = 'Wi33J3WxSDxWsrxLREcQqmO3iJ0dk52N'
    url = 'http://api.giphy.com/v1/gifs/search?q='+query+'&api_key=' + api + '&limit=500&rating=r'    
    data = json.loads(urllib2.urlopen(url).read())
    randno = randint(0,499)
    try:
        id = data['data'][randno]['id']
        gif = 'https://media2.giphy.com/media/'+id+'/giphy.gif'
    except IndexError:
        gif = ""
    return gif

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
