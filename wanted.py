import sopel.module

@sopel.module.commands('wanted')
def wanted(bot,trigger):
    if trigger.group(2):
        bot.say(trigger.group(2).strip() + " was never wanted as a child, but now is wanted in 37 states!")
