import sopel.module
@sopel.module.interval(5)
def spam_every_5s(bot):
    if "##test" in bot.channels:
        bot.msg("##test", "It has been five seconds!")
