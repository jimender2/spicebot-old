import sopel.module

@sopel.module.commands('homer')
def homer(bot,trigger):
	bot.say("D'ooooh!")
