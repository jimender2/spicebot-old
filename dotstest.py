import sopel.module

@sopel.module.commands('..','...','....')
def dots(bot,trigger):
    bot.say(trigger.nick + " used dots.")
