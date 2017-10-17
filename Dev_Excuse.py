import sopel.module
import urllib
from xml.dom.minidom import parseString

@sopel.module.rate(120)
@sopel.module.commands('devexcuse')
def devexcuse(bot, input):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        bot.say(parseString(
            urllib.urlopen('http://developerexcuses.com').read().replace('&', '')).
            getElementsByTagName('body')[0].getElementsByTagName('div')[0].
            getElementsByTagName('center')[0].getElementsByTagName('a')[0].
            childNodes[0].nodeValue)

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
