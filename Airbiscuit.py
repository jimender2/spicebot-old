import sopel.module

@sopel.module.commands('airbiscuit','float')
def airbiscuit(bot,trigger):
    bot.say(trigger.nick + " floats an air biscuit.")
