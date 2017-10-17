import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('trust')
def trust(bot,trigger):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        if  not trigger.group(2):
            bot.say("Trust Doesn't Rust.")
        elif not trigger.group(2).strip() == bot.nick:
            bot.say("I just can't ever bring myself to trust " + trigger.group(2).strip() + " again. I can never forgive " + trigger.group(2).strip() + " for the death of my boy.")

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
