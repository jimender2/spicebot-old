import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('asimov')
def asimov(bot, trigger):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        bot.action('may not injure a human being or, through inaction, allow a human being to come to harm.')
        bot.action('must obey orders given it by human beings except where such orders would conflict with the First Law.')
        bot.action('must protect its own existence as long as such protection does not conflict with the First or Second Law.')
        bot.action('must comply with all chatroom rules.')

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
