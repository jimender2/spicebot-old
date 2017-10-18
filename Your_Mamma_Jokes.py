import sopel.module
import requests
import json

@sopel.module.rate(120)
@sopel.module.commands('urmom')
def sayJoke(bot,trigger):
    instigator = trigger.nick
    target = trigger.nick
    update_usertotal(bot, target)
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
        warned = bot.db.get_nick_value(target, 'spicebothour_warn') or 0
        if not warned:
            bot.notice(target + ", you have to run .spiceboton to allow her to listen to you.", instigator)
        else:
            bot.notice(target + ", it looks like your access to spicebot has been disabled for a while. Check out ##SpiceBotTest.", instigator)

def update_usertotal(bot, nick):
    usertotal = bot.db.get_nick_value(nick, 'spicebot_usertotal') or 0
    bot.db.set_nick_value(nick, 'spicebot_usertotal', usertotal + 1)

def getJoke():
    url = 'http://api.yomomma.info'
    try:
      page = requests.get(url)
      result = page.content
      jsonjoke = json.loads(result)
      joke = jsonjoke['joke']
    except ConnectionError:
      joke = "yo mamma is a horrible human being."
    return joke

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
