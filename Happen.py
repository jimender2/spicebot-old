import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('happen')
def happen(bot,trigger):
    if trigger.group(2):
        bot.say("Stop trying to make " + trigger.group(2) + " happen. It's not going to happen")
