import sopel.module
import requests
import json

@sopel.module.rate(120)
@sopel.module.commands('urmom')
def sayJoke(bot,trigger):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        joke = getJoke()
        if joke:
            if not trigger.group(2):
                bot.say(joke)
            elif not trigger.group(2).strip() == bot.nick:
                bot.say('Hey, ' + trigger.group(2).strip() + '! ' + joke)        
        else:
            bot.say('Please leave the mothers out of it.')
    else:
        instigator = trigger.nick
        bot.notice(target + ", you have to run .spiceboton to allow her to listen to you.", instigator)

def getJoke():
    url = 'http://api.yomomma.info'
    page = requests.get(url)
    result = page.content
    jsonjoke = json.loads(result)
    joke = jsonjoke['joke']
    return joke

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
