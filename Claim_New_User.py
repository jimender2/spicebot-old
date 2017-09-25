import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('pee','claim','urinate')
def pee(bot, trigger):
    if not trigger.group(2):
        claimed = "new user"
    else:
        claimed = trigger.group(2).strip()
    if not claimed == bot.nick:
        bot.say(trigger.nick + ' urinates on ' + claimed + '! Claimed!')
