import sopel.module
import random
import pyjokes

@sopel.module.rate(120)
@sopel.module.commands('pyjoke')
def pyjoke(bot, trigger):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        j1 = pyjokes.get_jokes(category='neutral')
        j2 = pyjokes.get_jokes(category='adult')
        bot.say(random.choice(j1 + j2))
    else:
        instigator = trigger.nick
        bot.notice(target + ", you have to run .spiceboton to allow her to listen to you.", instigator)
        
## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
