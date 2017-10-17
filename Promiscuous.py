import sopel.module
from random import random
from random import randint

@sopel.module.rate(120)
@sopel.module.commands('sexbot','cockbot','fuckbot')
def promiscuous(bot,trigger):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        rando = randint(2, 666)
        bot.say("Please insert " + str(rando) + " bitcoins, for that kind of service.")

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
