import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('challenge')
def challenge(bot,trigger):
    if trigger.group(2):
        bot.say(trigger.nick + " challenges " + trigger.group(2) + " to a duel.")
