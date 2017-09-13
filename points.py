import sopel.module
from random import random
from random import randint

@sopel.module.commands('points','pants')
def points(bot, trigger):
        rando = randint(1, 5)
        winner = trigger.group(2)
        bot.say(trigger.nick + ' awards ' + rando + ' to ' + winner)
