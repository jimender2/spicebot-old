import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('devescuse','devesxuse')
def learntospell(bot, trigger):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        bot.say('You typed .' + trigger.group(1) + ' , You may need to learn to spell.')

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
