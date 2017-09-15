import sopel.module
from sopel.tools.target import User, Channel

@sopel.module.commands('getchannels')
def getChannels(bot,trigger):
	for c in bot.channels:
		bot.say("You can find me in " + c)
@sopel.module.commands('getmembers')
def getMembers(bot,trigger):
    for u in bot.channels.users:
        bot.say(u + " is in here")
