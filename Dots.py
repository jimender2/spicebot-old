import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('..')
def dots(bot,trigger):
    bot.say("...")
