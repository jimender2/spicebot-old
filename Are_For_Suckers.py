import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('sucker','suckers')
def rules(bot, trigger):
    target = trigger.group(3) or trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        if not trigger.group(2):
            bot.say("Who/what are for suckers??")
        else:
            myline = trigger.group(2).strip()
            if not myline.lower() == bot.nick:
                if myline.endswith('s'):
                    bot.say(myline + ' are for suckers!!')
                else:
                    bot.say(myline + ' is for suckers!!')

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
