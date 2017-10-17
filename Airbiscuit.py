import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('airbiscuit','float','floats')
def airbiscuit(bot,trigger):
    target = trigger.group(3) or trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        instigator = trigger.nick
        update_usertotal(bot, target)
        if target == trigger.nick:
            bot.say(trigger.nick + " floats an air biscuit.")
    else:
        instigator = trigger.nick
        bot.notice(target + ", you have to run .spiceboton to allow her to listen to you.", instigator)

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable

def get_usertotal(bot, nick):
    userstotal = bot.db.get_nick_value(nick, 'spicebot_usertotal') or 0
    return userstotal

def update_usertotal(bot, nick):
    userstotal = get_usertotal(bot, nick)
    bot.db.set_nick_value(nick, 'spicebot_usertotal', userstotal + 1)
