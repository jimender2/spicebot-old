import sopel.module
from random import random
from random import randint
from sopel import module, tools

@sopel.module.rate(120)
@sopel.module.commands('points','takepoints','pants','takepants','minuspants','minuspoints')
def points_cmd(bot, trigger):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        commandused = trigger.group(1)
        if commandused == 'points' or commandused == 'pants':
            giveortake = ' gives '
            tofrom = ' to '
            addminus = 'up'
        else:
            giveortake = ' takes '
            tofrom = ' from '
            addminus = 'down'
        if commandused.endswith('points'):
            pointstype = 'points'
        else:
            pointstype = 'pants'
        return pointstask(bot, trigger.sender, trigger.nick, trigger.group(3) or '', giveortake, tofrom, addminus, pointstype)
    else:
        instigator = trigger.nick
        bot.notice(target + ", you have to run .spiceboton to allow her to listen to you.", instigator)
        
@sopel.module.commands('checkpoints','checkpants')
def checkpoints(bot, trigger):
    target = trigger.nick
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        commandused = trigger.group(1)
        if commandused.endswith('points'):
            pointstype = 'points'
        else:
            pointstype = 'pants'
        target = trigger.group(3) or trigger.nick
        points = get_points(bot, target)
        if not points:
            bot.say(target + ' has no ' + pointstype + ' history.')
        else:
            bot.say(target + ' has ' + str(points) + ' ' + pointstype + '.')
    else:
        instigator = trigger.nick
        bot.notice(target + ", you have to run .spiceboton to allow her to listen to you.", instigator)
        
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

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
