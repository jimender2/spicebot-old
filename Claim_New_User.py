import sopel.module

@sopel.module.commands('pee','claim')
def pee(bot, trigger):
    if not trigger.group(2):
        winner = "new user"
    else:
        winner = trigger.group(2).strip()
    bot.say(trigger.nick + ' urinates on ' + winner + '!')
    bot.say('Claimed!')
