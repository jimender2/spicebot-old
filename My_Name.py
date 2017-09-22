import sopel.module

@sopel.module.commands(bot.nick)
def name(bot,trigger):
    bot.say("That's my name. Don't wear it out!")
