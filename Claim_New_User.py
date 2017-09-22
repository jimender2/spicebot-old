import sopel.module

@sopel.module.commands('pee','claim','urinate')
def pee(bot, trigger):
    if not trigger.group(2):
        winner = "new user"
    else:
        winner = trigger.group(2).strip()
    if not winner.lower() == 'spicebot':
        bot.say(trigger.nick + ' urinates on ' + winner + '!')
        bot.say('Claimed!')
