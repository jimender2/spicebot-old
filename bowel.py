import sopel.module

@sopel.module.commands('poop','poops')
def pee(bot, trigger):
    if not trigger.group(2):
        winner = "in the designated corner"
    else:
        winner = trigger.group(2).strip()
    if winner == "in the designated corner":
        bot.say(trigger.nick + ' poops ' + winner + '!')
    else:
        if myline.endswith('desk'):
            bot.say(trigger.nick + ' poops on ' + winner + ', maintaining eye contact the entire time!')
        else:
            bot.say(trigger.nick + ' poops on ' + winner + ' desk, maintaining eye contact the entire time!')
