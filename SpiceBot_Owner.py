import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('owner','botowner')
def botowner(bot,trigger):
    bot.say(bot.config.core.owner)
