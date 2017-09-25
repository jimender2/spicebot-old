import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('sucker','suckers')
def rules(bot, trigger):
    if not trigger.group(2):
        bot.say("Who/what are for suckers??")
    else:
        myline = trigger.group(2).strip()
        if not myline.lower() == bot.nick:
            if myline.endswith('s'):
                bot.say(myline + ' are for suckers!!')
            else:
                bot.say(myline + ' is for suckers!!')
