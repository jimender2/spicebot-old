import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('boat')
def shouldbuyaboat(bot,trigger):
    bot.say(trigger.nick + " should buy a boat.")
