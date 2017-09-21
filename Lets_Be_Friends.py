import sopel.module

@sopel.module.commands('fuckyouspicebot','fuckspicebot','banspicebot','kickspicebot','hatespicebot','fuckoffspicebot')
def apology(bot, trigger):
    bot.say(trigger.nick + ", I'm sorry I offended you. Lets try to be friends.")
