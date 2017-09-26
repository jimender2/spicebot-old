import sopel.module
from random import random
from random import randint

@sopel.module.rate(120)
@sopel.module.commands('points','pants')
def points(bot, trigger):
    whichtrig = trigger.group(1)    
    rando = randint(1, 666)
    if not trigger.group(2):
        winner = "Everybody"
    else:
        winner = trigger.group(2).strip()
    randopoints = ('is awarded ' + str(rando) + ' ' + whichtrig + ' from' )
    if winner == trigger.nick:
        bot.say('You can\'t give yourself ' + whichtrig + '!')
    else:
        bot.say(winner + ' ' + randopoints + ' ' + trigger.nick)

@sopel.module.rate(120)
@sopel.module.commands('takepoints','takepants')
def takepoints(bot, trigger):   
    rando = randint(1, 666)
    if not trigger.group(2):
        winner = "Everybody"
    else:
        winner = trigger.group(2).strip()
    randopoints = ('loses ' + str(rando) + ' points')
    if winner == trigger.nick:
        bot.say('You can\'t take your own points away!')
    else:
        bot.say(winner + ' ' + randopoints)
