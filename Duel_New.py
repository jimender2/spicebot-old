import sopel
from sopel import module, tools
import random

@sopel.module.commands('challenge')
def challenge(bot,trigger):
    if trigger.group(2):
        bot.say(trigger.nick + " challenges " + trigger.group(2) + " to a duel.")
    else:
        bot.say(trigger.nick + ", Who did you want to duel?")
 
@module.rule('^(?:challenges|(?:fi(?:ght|te)|duel)s(?:\s+with)?)\s+([a-zA-Z0-9\[\]\\`_\^\{\|\}-]{1,32}).*')
@module.intent('ACTION')
def duel_action(bot, trigger):
    bot.say(trigger.group(1))
    return duel(bot, trigger.sender, trigger.nick, trigger.group(1), is_admin=trigger.admin, warn_nonexistent=False)

@sopel.module.commands('duelnew')
def duel_cmd(bot, trigger):
    bot.say(str(bot))
    return duel(bot, trigger.sender, trigger.nick, trigger.group(3) or '', is_admin=trigger.admin)

def duel(bot, channel, instigator, target, is_admin=False, warn_nonexistent=True):
    target = tools.Identifier(target or '')
    if not target:
        bot.say("Who did you want to duel?")
    else:
        bot.say("instigator is: " + instigator)
        bot.say("target is: " + target)


def duelworks(bot,trigger):
    if trigger.group():
        if trigger.group(2) == bot.nick:
            bot.say("I refuse to duel with the yeller-bellied likes of you!")
        elif trigger.group(2) == trigger.nick:
            bot.say("You can't duel yourself, you coward!")
        else:
            bot.say(trigger.nick + " versus " + trigger.group(2) + ", loser's a yeller belly!")
            contestants  = [trigger.nick , trigger.group(2)]
            winner = random.randint(0,len(contestants) - 1)
            winner = str(contestants [winner])
            if winner == trigger.nick:
                loser = trigger.group(2)
            else:
                loser = trigger.nick
            bot.say(winner + " wins!")
            bot.say(winner + " done killed ya, " + loser)
    else:
        bot.say(trigger.nick + ", Who did you want to duel?")

#def weaponofchoice():
