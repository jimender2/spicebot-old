import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('spicebotmodules')
def spicemodules(bot, trigger):
    bot.say('Spiceworks IRC Modules     https://github.com/deathbybandaid/sopel-modules')
