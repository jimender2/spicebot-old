import sopel.module

@sopel.module.commands('tap')
def canYouSeeMe(bot,trigger):
    bot.say("*Tap, Tap* ...is this thing on?")
