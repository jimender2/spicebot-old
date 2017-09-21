import sopel.module

@sopel.module.commands('rimshot')
def rimshot(bot, trigger):
    #bot.action('uses drumsticks to hit both the head and the rim of the drum, then the cymbal.')
    bot.say('*Ba Dum Tss!!!*')
