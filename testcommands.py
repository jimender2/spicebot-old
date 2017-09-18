import sopel.module
from sopel.tools.target import User, Channel

@sopel.module.commands('getchannels')
def getChannels(bot,trigger):
	for c in bot.channels:
		bot.say("You can find me in " + c)
@sopel.module.commands('getmembers')
def getMembers(bot,trigger):
    for c in bot.channels:
        bot.say(c.users)
	
        #for u in c.users:
            #bot.say(u + " is here")
