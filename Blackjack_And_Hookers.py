import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('myown')
def bender(bot,trigger):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        if trigger.group(2):
            if not trigger.group(2) == bot.nick:
                bot.say("Fine! I'll start my own " + trigger.group(2) + ", with blackjack and hookers!")

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
