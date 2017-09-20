import sopel.module

@sopel.module.commands('poop','poops')
def pee(bot, trigger):
    if not trigger.group(2):
        myline = "in the designated corner"
    elif trigger.group(2) == 'all' or trigger.group(2) == 'everyone':
        myline = 'everyone'
    elif trigger.group(2) == 'group':
        myline = 'poopgroup'
    else:
        myline = trigger.group(2).strip()
    if myline == "in the designated corner":
        bot.say(trigger.nick + ' poops ' + myline + '!')
    elif myline == "everyone":
        bot.say(trigger.nick + ' poops on ' + myline + '\'s desk, one at a a time!')
    elif myline == "poopgroup":
        bot.say(trigger.nick + ' get your poop in a group.')
    else:
        if myline.endswith('desk'):
            bot.say(trigger.nick + ' poops on ' + myline + ', maintaining eye contact the entire time!')
        else:
            bot.say(trigger.nick + ' poops on ' + myline + '\'s desk, maintaining eye contact the entire time!')
