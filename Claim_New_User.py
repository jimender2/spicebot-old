import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('pee','claim','urinate')
def pee(bot, trigger):
    instigator = trigger.nick
    target = trigger.nick
    update_usertotal(bot, target)
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        if not trigger.group(2):
            claimed = "new user"
        else:
            claimed = trigger.group(2).strip()
        if not claimed == bot.nick and not claimed == trigger.nick:
            if trigger.nick == 'IT_Sean':
                bot.say(trigger.nick + ' releases the contents of his bladder on ' + claimed + '! All should recognize this profound claim of ownership upon ' + claimed +'!')
            else:
                bot.say(trigger.nick + ' urinates on ' + claimed + '! Claimed!')
    else:
        instigator = trigger.nick
        warned = bot.db.get_nick_value(target, 'spicebothour_warn') or 0
        if not warned:
            bot.notice(target + ", you have to run .spiceboton to allow her to listen to you.", instigator)
        else:
            bot.notice(target + ", it looks like your access to spicebot has been disabled for a while. Check out ##SpiceBotTest.", instigator)

def update_usertotal(bot, nick):
    usertotal = bot.db.get_nick_value(nick, 'spicebot_usertotal') or 0
    bot.db.set_nick_value(nick, 'spicebot_usertotal', usertotal + 1)
