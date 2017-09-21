import sopel.module

@sopel.module.commands('trust')
def trust(bot,trigger):
    if trigger.group(2):
        bot.say("I just can't ever bring myself to trust " + trigger.group(2).strip() + " again. I can never forgive " + trigger.group(2).strip() + for the death of my boy.")
    else:
        bot.say("Trust Doesn't Rust.")
