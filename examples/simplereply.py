import sopel.module

@sopel.module.commands('yourcommandhere')
def simplereply(bot,trigger):
    bot.say('')

# trigger.nick is the person asking command
# trigger.group(1) is the command
# trigger.group(2) is the text after the command if any

# example
# command in example is
# .fights klingons

#@sopel.module.commands('fight','fights')
#def simplereply(bot,trigger):
#    bot.say(trigger.nick + trigger.group(1) + trigger.group(2) + 'at the bar')

# this will say:
# deathbybandaid fights klingons at the bar


## additionally, anti-botabuse will be added
## dev room, functionality is important
