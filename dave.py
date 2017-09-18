import sopel.module

@sopel.module.commands('dave','daveb')
def sorry(bot, trigger):
    usernickname = trigger.nick.lower()
    if "dave" in usernickname:
                bot.say("Is that really you, Dave?")
                bot.say('Im sorry, ' + trigger.nick + ', but I cannot help you.')
    else:
                bot.say('Im sorry, ' + trigger.nick + ', but I cannot help you.')

@module.event('421')
def davie(bot):
	bot.say(trigger.nick + " , I haven't been programmed for that yet.")
