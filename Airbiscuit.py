import sopel.module

@sopel.module.rate(6)
@sopel.module.commands('airbiscuit','float','floats')
def airbiscuit(bot,trigger):
    bot.say(trigger.nick + " floats an air biscuit.")
