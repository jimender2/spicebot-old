import sopel.module
import random

@sopel.module.rate(560)
@sopel.module.commands('duelnew')
def duel(bot,trigger):
    if trigger.group():
        if trigger.group(2) == bot.nick:
            bot.say("I refuse to duel with the yeller-bellied likes of you!")
        elif trigger.group(2) == trigger.nick:
            bot.say("You can't duel yourself, you coward!")
        else:
            bot.say(trigger.nick + " versus " + trigger.group(2) + ", loser's a yeller belly!")
            contestants  = ["trigger.nick" , "trigger.group(2)"]
            winner = random.randint(0,len(contestants) - 1)
            loser = str(int(winner) - 1)
            winner = str(contestants [winner])
            loser = str(contestants [loser])
            bot.say(winner + " wins!")
            bot.say(winner + " done killed ya, " + loser)
    else:
        bot.say(trigger.nick + ", Who did you want to duel?")
