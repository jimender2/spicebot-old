import sopel.module

@sopel.module.commands('wanted')
def wanted(bot,trigger):
	bot.say(trigger.nick + " was never wanted as a child, but now is wanted in 37 states!")
