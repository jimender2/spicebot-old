import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('airbiscuit','float','floats')
def airbiscuit(bot,trigger):
    instigator = trigger.nick
    target = trigger.nick
    update_usertotal(bot, target)
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        if target == trigger.nick:
            bot.say(trigger.nick + " floats an air biscuit.")
    else:
        instigator = trigger.nick
        warned = bot.db.get_nick_value(target, 'spicebothour_warn') or 0
        if warned:
            bot.notice(target + ", it looks like your access to spicebot has been disabled for a while. Check out ##SpiceBotTest.", instigator)
        else:
            bot.notice(target + ", you have to run .spiceboton to allow her to listen to you.", instigator)

def update_usertotal(bot, nick):
    usertotal = bot.db.get_nick_value(nick, 'spicebot_usertotal') or 0
    bot.say(str(usertotal))
    bot.db.set_nick_value(nick, 'spicebot_usertotal', usertotal + 1)
    
## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
