import sopel.module
from random import random
from random import randint

@sopel.module.rate(120)
@sopel.module.commands('sexbot','cockbot','fuckbot')
def promiscuous(bot,trigger):
    rando = randint(2, 666)
    bot.say("Please insert " + str(rando) + " bitcoins, for that kind of service.")
