import sopel.module
from random import random
from random import randint

@sopel.module.commands('points','pants')
def points(bot, trigger):
        rando = randint(1, 666)
        # Not real sure if this next line is necessary, may leave it out and see if it works. - Z
        #rando = str(rando).encode('ascii','ignore').decode('ascii')
        if not trigger.group(2):
                winner = "Everybody"
        else:
                winner = trigger.group(2).strip()
        #randopoints = ('is awarded' , rando , 'points from')
        #bot.say(winner , randopoints , trigger.nick)
        randopoints = ('is awarded ' + str(rando) + ' points from ' )
        if winner == trigger.nick:
                bot.say("You can't give yourself points!")
        else:
                bot.say(winner + ' ' + randopoints + ' ' + trigger.nick)
