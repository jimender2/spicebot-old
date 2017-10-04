import sopel.module
from random import random
from random import randint
from sopel import module, tools

@sopel.module.rate(120)
@sopel.module.commands('points','takepoints')
def points_cmd(bot, trigger):
    commandused = trigger.group(1)
    if commandused == 'points':
        giveortake = ' gives '
        tofrom = ' to '
        addminus = 'up'
    else:
        giveortake = ' takes '
        tofrom = ' from '
        addminus = 'down'
    return pointstask(bot, trigger.sender, trigger.nick, trigger.group(3) or '', giveortake, tofrom, addminus)
    
    
def pointstask(bot, channel, instigator, target, giveortake, tofrom, addminus):
    target = tools.Identifier(target or '')
    rando = randint(1, 666)
    randopoints = (instigator + str(giveortake) + str(rando) + ' points' + str(tofrom) + ' ')    
    if not target:
        for u in bot.channels[channel].users:
            target = u
            bot.say(str(randopoints) + str(u))
            points_finished(bot, target, rando, addminus)
    else:
        if target == 'all' or target == 'everybody' or target == 'everyone':
            for u in bot.channels[channel].users:
                bot.say(str(randopoints) + str(u))
        if target == instigator:
            bot.say('You can\'t adjust your own points!!')
        elif target.lower() not in bot.privileges[channel.lower()]:
            bot.say("I'm not sure who that is.")
        else:
            bot.say(str(randopoints) + target)

def points_finished(bot, target, rando, addminus):
    if addminus == 'up':
        update_points(bot, target, rando, True)
    else:
        update_points(bot, target, rando, False)

def update_points(bot, target, rando, won=True):
    points = get_points(bot, nick)
    if won:
        bot.db.set_nick_value(nick, 'points_points', points + rando)
    else:
        bot.db.set_nick_value(nick, 'points_points', points - rando)

#def mypoints():
    
    
def get_points(bot, nick):
    points = bot.db.get_nick_value(nick, 'points_points') or 300
    return points
