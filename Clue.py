import sopel.module
import sys
import os
import random
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('clue')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)

rooms = ['Ballroom', 'Billiard Room', 'Cellar', 'Conservatory', 'Dining Room', 'Kitchen', 'Hall', 'Library', 'Lounge', 'Study', 'secret passage']
weapons = ['Candlestick', 'Knife', 'Lead Pipe', 'Revolver', 'Rope', 'Wrench', 'Wrench']
    
def execute_main(bot, trigger):
    players = []
    for c in bot.channels:
        channel = c
    for u in bot.channels[channel].users:
        target = u
        disenable = get_botdatabase_value(bot, target, 'disenable')
        if disenable:
            players.append(target)
    random.shuffle(rooms)
    random.shuffle(weapons)
    random.shuffle(players)
    if rooms[0] == 'secret passage':
        bot.say(players[2] + " evaded " + players[0] + " by using the secret passage. So " + players[0] + " killed " + players[1] + " with the " + weapons[0] + " instead.")    
    else:
        bot.say(players[0] + " killed " + players[1] + " in the " + rooms[0] + " with the " + weapons[0] + ".")
    import Points
    if trigger.group(3):
        if trigger.group(4):
            if trigger.group(4) == 'killer' and trigger.group(3) == players[0]:
                bot.say('You guessed the killer correctly!')
                Points.pointstask(bot, channel, 'SpiceBot', trigger.nick, ' gives ', ' to', 'up', 'points', trigger.sender)
            elif trigger.group(4) == 'killed' and trigger.group(3) == players[1]:
                bot.say('You guessed the person murdered!')
                Points.pointstask(bot, channel, 'SpiceBot', trigger.nick, ' gives ', ' to', 'up', 'points', trigger.sender)
        if trigger.group(3) == players[0]:
            bot.say('You guessed the killer correctly!')
            Points.pointstask(bot, channel, 'SpiceBot', trigger.nick, ' gives ', ' to', 'up', 'points', trigger.sender)
    if players[0] == trigger.nick:
        bot.say('You were the killer.')
        Points.pointstask(bot, channel, 'SpiceBot', trigger.nick, ' takes ', ' from', 'down', 'points', trigger.sender)
