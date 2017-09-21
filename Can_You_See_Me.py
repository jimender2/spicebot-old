import sopel.module

@sopel.module.commands('canyouseeme')
def canYouSeeMe(bot,trigger):
	bot.say(trigger.nick + " , I can see you.")
