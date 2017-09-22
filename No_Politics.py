import sopel.module

@sopel.module.commands('sign','politics','religion')
def sign(bot,trigger):
    bot.say("NO POLITICS OR RELIGION IN #spiceworks!")
