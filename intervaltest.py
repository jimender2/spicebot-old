import sopel.module
@sopel.module.interval(60)
def spam_every_60s(bot):
    if "##test" in bot.channels:
        bot.msg("##test", "It has been 60 seconds!")
