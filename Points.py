import sopel.module
from random import random
from random import randint

@sopel.module.rate(120)
@sopel.module.commands('points')
def points_cmd(bot, trigger):
    return points(bot, trigger.sender, trigger.nick, trigger.group(3) or '')
    
    
def points(bot, channel, instigator, target, whichtrig, warn_nonexistent=True):
    target = tools.Identifier(target or '')
    rando = randint(1, 666)
    randopoints = ('is awarded ' + str(rando) + ' ' + whichtrig + ' from' + instigator)
    if not target:
        for u in bot.channels[channel].users:
            bot.say(u)

    

    
    
    #if not trigger.group(2):
    #    loser = "Everybody"
    #else:
    #    loser = trigger.group(2).strip()
    #    if trigger.group(2) == 'all':
    #        loser = "Everybody"
    #if loser == trigger.nick:
    #    bot.say('You can\'t give yourself ' + whichtrig + '!')
    #else:
    #    rando = randint(1, 666)
    #    randopoints = ('is awarded ' + str(rando) + ' ' + whichtrig + ' from' )
    #    bot.say(loser + ' ' + randopoints + ' ' + trigger.nick)

@sopel.module.rate(120)
@sopel.module.commands('takepoints','takepants','minuspants','minuspoints')
def takepoints(bot, trigger):   
    if not trigger.group(2):
        winner = "Everybody"
    else:
        winner = trigger.group(2).strip()
        if trigger.group(2) == 'all':
            winner = "Everybody"
    if winner == trigger.nick:
        bot.say('You can\'t take your own points away!')
    else:
        rando = randint(1, 666)
        randopoints = ('loses ' + str(rando) + ' points')
        bot.say(winner + ' ' + randopoints)

@sopel.module.rate(120)
@sopel.module.commands('pints','pint')
def pints(bot, trigger):
    if not trigger.group(2):
        winner = "Everybody"
    else:
        winner = trigger.group(2).strip()
        if trigger.group(2) == 'all':
            winner = "Everybody"
        elif trigger.group(2) == trigger.nick:
            winner = "him/her-self"
    bot.say(trigger.nick + ' buys a pint for ' + winner)
