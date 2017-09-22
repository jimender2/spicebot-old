import sopel.module

@sopel.bot.Sopel(bot.nick)
def name(bot,trigger):
    bot.say("That's my name. Don't wear it out!")
