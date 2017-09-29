import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('halp')
def halp(bot,trigger):
    bot.say("If you need help using help you are truly lost.")
