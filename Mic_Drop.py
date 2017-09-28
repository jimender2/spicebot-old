import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('micdrop')
def micdrop(bot,trigger):
    bot.say(" ")
