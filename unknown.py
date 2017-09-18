import sopel.module

@sopel.module.event(events.ERR_UNKNOWNCOMMAND)
def davie(bot,trigger):
	bot.say(trigger.nick + " , I haven't been programmed for that yet.")
