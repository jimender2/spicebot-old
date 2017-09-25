import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('sign','politics','religion')
def sign(bot,trigger):
    bot.say("NO POLITICS OR RELIGION IN #spiceworks!")
