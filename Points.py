import sopel.module
from random import random
from random import randint
from sopel import module, tools

@sopel.module.rate(120)
@sopel.module.commands('points')
def points_cmd(bot, trigger):
    commandused = trigger.group(1)
    if commandused == 'points':
        giveortake = 'gives'
        tofrom = 'to'
    else:
        giveortake = 'takes'
        tofrom = 'from'
    return points(bot, trigger.sender, trigger.nick, trigger.group(3) or '', giveortake, tofrom)
    
    
def points(bot, channel, instigator, target, giveortake, tofrom, warn_nonexistent=True):
    target = tools.Identifier(target or '')
    rando = randint(1, 666)
    randopoints = (instigator + str(giveortake) + str(rando) + ' points ' + str(tofrom) + ' ')    
    if not target:
        for u in bot.channels[channel].users:
            bot.say('this will be: ' + str(randopoints) + str(u))
    else:
        if target == 'all' or target == 'everybody' or target == 'everyone':
            for u in bot.channels[channel].users:
                bot.say('this will be: ' + str(randopoints) + str(u))
        if target == instigator:
            bot.say('You can\'t adjust your own points!!')
        elif target.lower() not in bot.privileges[channel.lower()]:
            bot.say("I'm not sure who that is.")
        else:
            bot.say('this will be: ' + str(randopoints) + target)
