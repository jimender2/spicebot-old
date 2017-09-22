import sopel.module

@sopel.module.commands('poop','poops')
def poop(bot, trigger):
    if not trigger.group(2):
        bot.say(trigger.nick + ' poops in the designated corner!')
    elif trigger.group(2) = 'group':
            bot.say(trigger.nick + ', get your poop in a group.')
    elif trigger.group(2) == 'all' or trigger.group(2) == 'everyone' or trigger.group(2) == 'everyones':
            bot.say(trigger.nick + " poops on everyone's desk, one at a time!")
    elif not trigger.group(2) == bot.nick:
        myline = trigger.group(2).strip()
        if myline.endswith('desk'):
            bot.say(trigger.nick + ' poops on ' + myline + ', maintaining eye contact the entire time!')
        else:
             ot.say(trigger.nick + ' poops on ' + myline + '\'s desk, maintaining eye contact the entire time!')
