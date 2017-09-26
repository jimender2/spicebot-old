import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('phish','catphish')
def phis(bot,trigger):
	bot.say("A/S/L ??")
