import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('flush')
def flush(bot, trigger):
    #bot.action('jiggles toilet tank lever.')
    bot.say('*splsssssssssssssshhhhhhh gurgle gurgle gurgle*')
