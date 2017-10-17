import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('canyouseeme')
def canYouSeeMe(bot,trigger):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        bot.say(trigger.nick + " , I can see you.")

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
