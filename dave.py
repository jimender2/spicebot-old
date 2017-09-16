import sopel.module

@sopel.module.commands('dave','daveb')
def sorry(bot, trigger):
    if trigger.nick == Dave or trigger.nick == dave:
                bot.say("Is that really you, Dave?")
                bot.say('I'm sorry, ' , trigger.nick , 'but I cannot help you.'
    else:
                bot.say('I'm sorry, ' , trigger.nick , 'but I cannot help you.'
