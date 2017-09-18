import sopel.module

@sopel.module.event(events.ERR_UNKNOWNCOMMAND)
def davie(bot):
	bot.say(trigger.nick + " , I haven't been programmed for that yet.")
