import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('pints','pint')
def pints(bot, trigger):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        if not trigger.group(2):
            winner = "Everybody"
        else:
            winner = trigger.group(2).strip()
            if trigger.group(2) == 'all':
                winner = "Everybody"
            elif trigger.group(2) == trigger.nick:
                winner = "him/her-self"
        bot.say(trigger.nick + ' buys a pint for ' + winner)
    else:
        instigator = trigger.nick
        bot.notice(target + ", you have to run .spiceboton to allow her to listen to you.", instigator)
        
## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
