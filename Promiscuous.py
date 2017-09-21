import sopel.module
from random import random
from random import randint

@sopel.module.commands('sexbot','cockbot')
def promiscuous(bot,trigger):
    rando = randint(2, 666)
    bot.say("Please insert " + rando " bitcoins, for that kind of service.")
