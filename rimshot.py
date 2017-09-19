import sopel.module

@sopel.module.commands('rimshot')
def rimshot(bot, trigger):
    bot.say('Ba Dum Tss!!!')
