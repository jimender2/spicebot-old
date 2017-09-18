import sopel.module

@sopel.module.commands('fuckyouspicebot','fuckspicebot','banspicebot','kickspicebot','hatespicebot')
def apology(bot, trigger):
    bot.say(trigger.nick + ', I'm sorry I offended you. Can we try to be friends\?')
