import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('owner','botowner')
def botowner(bot,trigger):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        bot.say(bot.config.core.owner)

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
