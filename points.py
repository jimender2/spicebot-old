import sopel.module
from random import random
from random import randint

@sopel.module.commands('points','pants')
def points(bot, trigger):
        rando = randint(1, 666)
        winner = trigger.group(2)
        randopoints = ('is awarded' , str(rando) , 'points from')
        bot.say(winner , randopoints , trigger.nick)
