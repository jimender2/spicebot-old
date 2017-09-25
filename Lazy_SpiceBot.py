import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('lazy','lazyfuckingspicebot','fuckinglazyspicebot','lazyspicebot')
def lazy(bot, trigger):
    bot.say('I do not tell you how to do your job, ' + trigger.nick + '!!')
