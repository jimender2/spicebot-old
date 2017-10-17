import sopel.module

@sopel.module.rate(120)
@sopel.module.commands('pee','claim','urinate')
def pee(bot, trigger):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        if not trigger.group(2):
            claimed = "new user"
        else:
            claimed = trigger.group(2).strip()
        if not claimed == bot.nick and not claimed == trigger.nick:
            if trigger.nick == 'IT_Sean':
                bot.say(trigger.nick + ' releases the contents of his bladder on ' + claimed + '! All should recognize this profound claim of ownership upon ' + claimed +'!')
            else:
                bot.say(trigger.nick + ' urinates on ' + claimed + '! Claimed!')
