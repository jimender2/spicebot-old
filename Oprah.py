import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('oprah')
def trust(bot,trigger):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        if trigger.group(2):
            item = trigger.group(2).strip()
            if item.startswith('a') or item.startswith('e') or item.startswith('i') or item.startswith('o') or item.startswith('u'):
                item = str('an ' + item)
            else:
                item = str('a ' + item)
            bot.say("You get " + item + "! And You get " + item + "! Everyone gets "+ item + "!")

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
