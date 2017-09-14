import sopel.module
from random import random
from random import randint

@sopel.module.commands('points','pants')
def points(bot, trigger):
        rando = randint(1, 666)
        # Not real sure if this next line is necessary, may leave it out and see if it works. - Z
        #rando = str(rando).encode('ascii','ignore').decode('ascii')
        winner = trigger.group(2)
        #randopoints = ('is awarded' , rando , 'points from')
        #bot.say(winner , randopoints , trigger.nick)
        randopoints = (' is awarded ' + str(rando) + ' points from ' )
        bot.say(winner + ' ' + randopoints + ' ' + trigger.nick)
