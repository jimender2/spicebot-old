import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('thump','thumps')
def thump(bot, trigger):
    if not trigger.group(2):
        bot.say("Did you mean to thump somebody?")
    elif not trigger.group(2).strip() == bot.nick:
        bot.action('thumps ' + trigger.group(2).strip() + ' on behalf of ' + trigger.nick)
