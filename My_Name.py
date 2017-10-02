import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('spicebot','spicebotdev','spicebot ','spicebotdev ')
def name(bot,trigger):
    bot.say("That's my name. Don't wear it out!")
