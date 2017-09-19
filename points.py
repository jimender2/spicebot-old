from sopel import module
from random import random
from random import randint

def points(bot, trigger):
    whichtrig = trigger.group(1)    
    rando = randint(1, 666)
    if not trigger.group(2):
        winner = "Everybody"
    else:
        winner = trigger.group(2).strip()
    randopoints = ('is awarded ' + str(rando) + whichtrig + ' from' )
    if winner == trigger.nick:
        bot.say("You can't give yourself points!")
    else:
        bot.say(winner + ' ' + randopoints + ' ' + trigger.nick)
points.commands = ['points','pants']
