import sopel.module
from random import random
from random import randint

@sopel.module.commands('wanted')
def wanted(bot,trigger):
    rando = randint(2, 50)
    if trigger.group(2):
        bot.say(trigger.group(2).strip() + " was never wanted as a child, but now is wanted in ' + str(rando) + ' states!")
