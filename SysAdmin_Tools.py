import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('sysadmintools')
def sysadmintools(bot, trigger):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        bot.say('https://sysadmin.it-landscape.info/     https://sysadmin.libhunt.com/     https://github.com/n1trux/awesome-sysadmin')

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
