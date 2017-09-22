import sopel.module

botnick = getbotnick(bot)

@sopel.module.commands(botnick)
def name(bot,trigger):
    bot.say("That's my name. Don't wear it out!")

def getbotnick(bot):
    botnick = bot.nick
    return botnick
