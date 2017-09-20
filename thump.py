import sopel.module

@sopel.module.commands('thump','thumps')
def thump(bot, trigger):
    if not trigger.group(2):
        bot.say("Did you mean to thump somebody?")
    else:
        bot.action('thumps ' + trigger.group(2) + ' on behalf of ' + trigger.nick)
