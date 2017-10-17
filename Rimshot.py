import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('rimshot')
def rimshot(bot, trigger):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        bot.action('uses drumsticks to hit both the head and the rim of the drum, then the cymbal.')
        bot.say('*Ba Dum Tss!!!*')

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
