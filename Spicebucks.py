import sopel.module
from sopel import module, tools
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

## All commands will use .spicebucks [action]
## Actions to include
### payday - Recieve a once a day payday amount (current Thought is 5 / day)
### bank - Check amount in bank
### transfer - Transfer money from one user to another

@sopel.module.commands('spicebucks')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    for c in bot.channels:
        channel = c
    commandused = trigger.group(3)
    inchannel = trigger.sender
    if commandused.startswith('payday'):
        bot.say('add payday money')
    elif commandused.startswith('bank'):
        bot.say('check amount in bank')
    elif commandused.startswith('transfer'):
        bot.say('transfer money to another user')
##### Lots to do

def spicebuckstransaction(bot, channel, instigator, target, addsubtract, amount, inchannel):
    ### use this to add or remove spicebucks from a user.  Returns True if successful, and False if unsuccessful
    ### keep do not use this for spicebot.say or notify.  Use the calling function to do that so that you can say whatever you want.
    
    

def pointstask(bot, channel, instigator, target, giveortake, tofrom, addminus, pointstype, inchannel):
    target = tools.Identifier(target or '')
    rando = randint(1, 666)
    randopoints = (instigator + str(giveortake) + str(rando) + ' ' + pointstype + str(tofrom) + ' ')    
    if not target:
        bot.say(str(randopoints) + "everyone")
        channelpoints(bot, instigator, channel, rando, addminus)
    else:
        if target == 'all' or target == 'everybody' or target == 'everyone':
            if not inchannel.startswith("#"):
                bot.say('you must be in the room to give everyone points')
            else:
                bot.say(str(randopoints) + "everyone")
                channelpoints(bot, instigator, channel, rando, addminus)
        elif target == instigator:
            bot.say('You can\'t adjust your own ' + pointstype + '!!')
        elif target.lower() not in bot.privileges[channel.lower()]:
            bot.say("I'm not sure who that is.")
        else:
            bot.say(str(randopoints) + target)
            update_points(bot, target, rando, addminus)
            if target != instigator and not inchannel.startswith("#"):
                bot.notice(str(randopoints) + target, target)
            
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
