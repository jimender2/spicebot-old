import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('homer')
def homer(bot,trigger):
	bot.say("D'ooooh!")
