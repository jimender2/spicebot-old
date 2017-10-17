import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('spicebotmodules')
def spicemodules(bot, trigger):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        bot.say('Spiceworks IRC Modules     https://github.com/deathbybandaid/sopel-modules')

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
