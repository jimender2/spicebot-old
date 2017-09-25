import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('optest')
def optest(bot,trigger):
    if not trigger.operator:
        bot.say('you are not op')
