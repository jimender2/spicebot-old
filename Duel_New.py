import sopel
from sopel import module, tools
import random

#@sopel.module.commands('challenge')
#def challenge(bot,trigger):
#    if trigger.group(2):
#        return duel(bot, trigger.sender, trigger.nick, trigger.group(3) or '', is_admin=trigger.admin)
#    else:
#        bot.say(trigger.nick + ", Who did you want to duel?")
 
#@module.rule('^(?:challenges|(?:fi(?:ght|te)|duel)s(?:\s+with)?)\s+([a-zA-Z0-9\[\]\\`_\^\{\|\}-]{1,32}).*')
#@module.intent('ACTION')
#def duel_action(bot, trigger):
#    bot.say(trigger.group(1))
#    return duel(bot, trigger.sender, trigger.nick, trigger.group(1), is_admin=trigger.admin, warn_nonexistent=False)

@sopel.module.commands('challenge')
def duel_cmd(bot, trigger):
    return duel(bot, trigger.sender, trigger.nick, trigger.group(3) or '', is_admin=trigger.admin)

def duel(bot, channel, instigator, target, is_admin=False, warn_nonexistent=True):
    target = tools.Identifier(target or '')
    if not target:
        bot.say(instigator + ", Who did you want to duel?")
    else:
        if target == bot.nick:
            bot.say("I refuse to duel with the yeller-bellied likes of you!")
        elif target == instigator:
            bot.say("You can't duel yourself, you coward!")
        else:
            bot.say(instigator + " versus " + target + ", loser's a yeller belly!")
            contestants  = [instigator , target]
            winner = random.randint(0,len(contestants) - 1)
            winner = str(contestants [winner])
            if winner == instigator:
                loser = target
            else:
                loser = instigator
            bot.say(winner + " wins!")
            bot.say(winner + " done killed ya, " + loser)

        

#def weaponofchoice():
