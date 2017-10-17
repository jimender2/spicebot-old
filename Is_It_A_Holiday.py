import sopel.module
import requests
import json

@sopel.module.rate(120)
@sopel.module.commands('isitaholiday')
def isitaholiday(bot,trigger):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        holiday = getholiday()
        if holiday:
            bot.say('Today is a holiday.')
        else:
            bot.say('Today is not a holiday.')
    else:
        instigator = trigger.nick
        bot.notice(target + ", you have to run .spiceboton to allow her to listen to you.", instigator)
        
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
