import sopel.module
import requests
import json

@sopel.module.rate(120)
@sopel.module.commands('isitaholiday')
def isitaholiday(bot,trigger):
    instigator = trigger.nick
    target = trigger.nick
    update_usertotal(bot, target)
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        holiday = getholiday()
        if holiday:
            bot.say('Today is a holiday.')
        else:
            bot.say('Today is not a holiday.')
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
        
def getholiday():
    url = 'http://isitaholiday.herokuapp.com/api/v2/holidays/today/'
    page = requests.get(url)
    result = page.content
    jsonholiday = json.loads(result)
    holiday = jsonholiday['status']
    return holiday

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
