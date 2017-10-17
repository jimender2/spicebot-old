import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('thump','thumps')
def thump(bot, trigger):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        if not trigger.group(2):
            bot.say("Did you mean to thump somebody?")
        elif not trigger.group(2).strip() == bot.nick:
            bot.action('thumps ' + trigger.group(2).strip() + ' on behalf of ' + trigger.nick)

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
