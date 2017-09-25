import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('sword','link','zelda')
def canYouSeeMe(bot,trigger):
	bot.say("it's dangerous to go alone take this 0==\======>")
