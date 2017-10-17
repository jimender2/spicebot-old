import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('flush')
def flush(bot, trigger):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        bot.action('jiggles toilet tank lever.')
        bot.say('*splsssssssssssssshhhhhhh gurgle gurgle gurgle*')

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
