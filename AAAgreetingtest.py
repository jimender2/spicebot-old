from sopel.module import event, rule

@event('JOIN')
@rule('.*')
def greeting(bot, trigger):
    bot.say("hello " + trigger.nick)
