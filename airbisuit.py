import sopel.module

@sopel.module.commands('airbisuit')
def airbisuit(bot,trigger):
    bot.say(trigger.nick + " floats an air biscuit.")
