import sopel.module

@sopel.module.commands('poop','poops')
def pee(bot, trigger):
    if not trigger.group(2):
        myline = "in the designated corner"
    else:
        myline = trigger.group(2).strip()
    if myline == "in the designated corner":
        bot.say(trigger.nick + ' poops ' + myline + '!')
    else:
        if myline.endswith('desk'):
            bot.say(trigger.nick + ' poops on ' + myline + ', maintaining eye contact the entire time!')
        else:
            bot.say(trigger.nick + ' poops on ' + myline + "'s desk, maintaining eye contact the entire time!")
