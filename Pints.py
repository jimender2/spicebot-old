import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('pints','pint')
def pints(bot, trigger):
    if not trigger.group(2):
        winner = "Everybody"
    else:
        winner = trigger.group(2).strip()
        if trigger.group(2) == 'all':
            winner = "Everybody"
        elif trigger.group(2) == trigger.nick:
            winner = "him/her-self"
    bot.say(trigger.nick + ' buys a pint for ' + winner)
