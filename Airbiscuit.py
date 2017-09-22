import sopel.module

@sopel.module.commands('airbiscuit','float','floats')
def airbiscuit(bot,trigger):
    bot.say(trigger.nick + " floats an air biscuit.")
