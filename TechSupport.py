import sopel.module
import random

@sopel.module.rate(120)
@sopel.module.commands('techsupport','itsupport')
def techsupport(bot, trigger):
    instigator = trigger.nick
    target = trigger.nick
    update_usertotal(bot, target)
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        messages = ["YOU MUST CONSTRUCT ADDITIONAL PYLONS!","Have you tried flinging feces at it?","Have you tried chewing the cable?","Did you try turning it off and on again?","Did you try licking the mouse? Double-lick?","Did your try replacing all the ones with zeros?"]
        answer = random.randint(0,len(messages) - 1)
        bot.say(messages[answer]);
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
