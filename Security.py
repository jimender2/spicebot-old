import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('security')
def airbiscuit(bot,trigger):
    bot.say("Does not compute.")
