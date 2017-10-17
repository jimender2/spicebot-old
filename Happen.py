import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('happen')
def happen(bot,trigger):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        if trigger.group(2):
            bot.say("Stop trying to make " + trigger.group(2) + " happen. It's not going to happen")

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
