import sopel.module
from random import random
from random import randint
from sopel import module, tools
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.rate(120)
@sopel.module.commands('points','takepoints','pants','takepants','minuspants','minuspoints','checkpoints','checkpants')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    commandused = trigger.group(1)
    target = trigger.group(3) or trigger.nick
    if commandused.endswith('points'):
        pointstype = 'points'
    else:
        pointstype = 'pants'
    if commandused.startswith('check'):
        points = get_points(bot, target)
        if not points:
            bot.say(target + ' has no ' + pointstype + ' history.')
        else:
            bot.say(target + ' has ' + str(points) + ' ' + pointstype + '.')
    else:
        if commandused.startswith('take') or commandused.startswith('minus'):
            giveortake = ' takes '
            tofrom = ' from '
            addminus = 'down'
        else:
            giveortake = ' gives '
            tofrom = ' to '
            addminus = 'up'      
        return pointstask(bot, trigger.sender, trigger.nick, trigger.group(3) or '', giveortake, tofrom, addminus, pointstype)

def pointstask(bot, channel, instigator, target, giveortake, tofrom, addminus, pointstype):
    target = tools.Identifier(target or '')
    rando = randint(1, 666)
    randopoints = (instigator + str(giveortake) + str(rando) + ' ' + pointstype + str(tofrom) + ' ')    
    if not target:
        bot.say(str(randopoints) + "everyone")
        channelpoints(bot, instigator, channel, rando, addminus)
    else:
        if target == 'all' or target == 'everybody' or target == 'everyone':
            bot.say(str(randopoints) + "everyone")
            channelpoints(bot, instigator, channel, rando, addminus)
        elif target == instigator:
            bot.say('You can\'t adjust your own ' + pointstype + '!!')
        elif target.lower() not in bot.privileges[channel.lower()]:
            bot.say("I'm not sure who that is.")
        else:
            bot.say(str(randopoints) + target)
            update_points(bot, target, rando, addminus)

def channelpoints(bot, instigator, channel, rando, addminus):
    for u in bot.channels[channel].users:
        errrbody = u
        if errrbody != instigator:
            update_points(bot, errrbody, rando, addminus)
            
def update_points(bot, nick, rando, addminus):
    pointsgotten = get_points(bot, nick)
    if addminus == 'up':
        bot.db.set_nick_value(nick, 'points_points', pointsgotten + int(rando))
    else:
        bot.db.set_nick_value(nick, 'points_points', pointsgotten - int(rando))

def get_points(bot, nick):
    points = bot.db.get_nick_value(nick, 'points_points') or 1
    return points
