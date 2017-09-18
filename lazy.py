import sopel.module

@sopel.module.commands('lazy','lazyfuckingspicebot')
def lazy(bot, trigger):
    bot.say('I do not tell you how to do your job, ' + trigger.nick)
