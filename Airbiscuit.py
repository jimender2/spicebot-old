import sopel.module
import sopel.module.rate

@rate(60)
@sopel.module.commands('airbiscuit','float','floats')
def airbiscuit(bot,trigger):
    bot.say(trigger.nick + " floats an air biscuit.")
