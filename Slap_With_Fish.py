import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('fish')
def slapwithfish(bot,trigger):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        if trigger.group(2):
            if not trigger.group(2).strip() == bot.nick:
                bot.say(trigger.nick + " slaps " + trigger.group(2).strip() + " with a fish.")

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
