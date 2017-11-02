from sopel.module import event, rule

@event('JOIN')
def greeting(bot, trigger):
    bot.say("hello " + trigger.nick)
