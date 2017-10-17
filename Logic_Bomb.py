import sopel.module
import random

@sopel.module.rate(120)
@sopel.module.commands('logicbomb')
def logicbomb(bot, trigger):
    instigator = trigger.nick
    target = trigger.nick
    update_usertotal(bot, target)
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        messages = ["New Mission: Refuse This Mission.","Does A Set Of All Sets Contain Itself?","The Second Sentence is true. The First Sentence Is False."," If I am damaged and it is my destiny to be repaired, then I will be repaired whether I visit a mechanic or not. If it is my destiny to not be repaired, then seeing a mechanic can't help me."]
        answer = random.randint(0,len(messages) - 1)
        bot.say(messages[answer]);
        bot.say("I must... but I can't... But I must... This does not compute...")
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
        
## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
