import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('rickroll')
def rickroll(bot, trigger):
    bot.say('This link is definately NOT a Rickroll     https://goo.gl/SsAhv')
