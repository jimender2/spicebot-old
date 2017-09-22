import sopel.module

def getbotnick():
    botnick = bot.nick
    return botnick

@sopel.module.commands(getbotnick())
def name(bot,trigger):
    bot.say("That's my name. Don't wear it out!")


