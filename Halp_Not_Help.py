import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('halp')
def halp(bot,trigger):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        bot.say("If you need help using help you are truly lost.")

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
