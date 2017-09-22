import sopel.module

def getbotnick(bot):
    botnick = bot.nick
    return botnick

@sopel.module.commands(getbotnick(bot))
def name(bot,trigger):
    bot.say("That's my name. Don't wear it out!")
