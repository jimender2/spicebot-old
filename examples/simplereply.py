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


#instigatordisenable = get_disenable(bot, instigator)
#targetdisenable = get_disenable(bot, target)

## Check Status of Opt In
#def get_disenable(bot, nick):
#    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
#    return disenable

## Check Opt-in Status
#        elif not instigatordisenable:
#            bot.say(instigator + ', It looks like you have disabled Challenges. Run .challengeon to re-enable.')
#        elif not targetdisenable:
#            bot.say(instigator + ', It looks like ' + target + ' has disabled Challenges.')
        
