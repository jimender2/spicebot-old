import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('pints','pint')
def pints(bot, trigger):
    if trigger.group(1).endswith('s'):
        quantity = 'pints'
    else:
        quantity = 'a pint'
    if not trigger.group(2):
        winner = "Everybody"
    else:
        winner = trigger.group(2).strip()
        if trigger.group(2) == 'all':
            winner = "Everybody"
        elif trigger.group(2) == trigger.nick:
            winner = "him/her-self"
    bot.say(trigger.nick + ' buys ' + quantity + ' for ' + winner)
