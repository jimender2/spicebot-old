import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('fuckyouspicebot','fuckspicebot','banspicebot','kickspicebot','hatespicebot','fuckoffspicebot')
def apology(bot, trigger):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        bot.say(trigger.nick + ", I'm sorry I offended you. Lets try to be friends.")
    else:
        instigator = trigger.nick
        bot.notice(target + ", you have to run .spiceboton to allow her to listen to you.", instigator)
        
## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
