import sopel.module

@sopel.module.commands('halp')
def halp(bot,trigger):
	bot.say("if you need help using help you are truly lost")
