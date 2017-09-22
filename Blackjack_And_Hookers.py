import sopel.module

@sopel.module.commands('myown')
def bender(bot,trigger):
    if trigger.group(2):
        if not trigger.group(2) == bot.nick:
            bot.say("Fine! I'll start my own " + trigger.group(2) + ", with blackjack and hookers!")
