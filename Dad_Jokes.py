import sopel.module
import requests

@sopel.module.rate(120)
@sopel.module.commands('dad','dadjoke')
def sayDadJoke(bot,trigger):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        joke = getDadJoke()
        if joke:
            bot.say(joke)
        else:
            bot.say('My humor module is broken.')
    else:
        instigator = trigger.nick
        bot.notice(target + ", you have to run .spiceboton to allow her to listen to you.", instigator)
        
def getDadJoke():
    url = 'https://icanhazdadjoke.com'    
    page = requests.get(url,headers = {'Accept':'text/plain'})
    joke = page.content
    return joke

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
