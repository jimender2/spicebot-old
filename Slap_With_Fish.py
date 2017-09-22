import sopel.module

@sopel.module.commands('fish')
def slapwithfish(bot,trigger):
    if not trigger.group(2) == bot.nick:
        bot.say(trigger.nick + " slaps " + trigger.group(2) + " with a fish.")
