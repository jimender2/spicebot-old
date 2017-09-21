import sopel.module

@sopel.module.commands('airbiscuit')
def airbiscuit(bot,trigger):
    bot.say(trigger.nick + " floats an air biscuit.")
