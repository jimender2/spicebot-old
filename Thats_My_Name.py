import sopel.module
from sopel.module import bot

@sopel.module.rate(120)
@sopel.module.commands(bot.nick)
def airbiscuit(bot,trigger):
    bot.say("That's my name, don't wear it out.")
