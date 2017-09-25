import sopel.module

@sopel.module.commands('optest')
def optest(bot,trigger):
    if not trigger.op:
        bot.say('you are not op')
