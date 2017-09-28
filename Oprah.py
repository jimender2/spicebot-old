import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('oprah')
def trust(bot,trigger):
    if trigger.group(2):
        bot.say("You get a " + trigger.group(2).strip() + "! And You get a " + trigger.group(2).strip() + "! Everyone gets a "+ trigger.group(2).strip() + "!")
