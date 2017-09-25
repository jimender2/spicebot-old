import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('redalert')
def redalert(bot, trigger):
    bot.say('Shields Up, Captain ' + trigger.nick)
