#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
import random
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

rooms = ['Ballroom', 'Billiard Room', 'Cellar', 'Conservatory', 'Dining Room', 'Kitchen', 'Hall', 'Library', 'Lounge', 'Study', 'secret passage', 'Spa', 'Theater', 'Nearby Guest House']
weapons = ['Candlestick', 'Knife', 'Lead Pipe', 'Revolver', 'Rope', 'Wrench', 'Dumbbell', 'Trophy', 'Poison']

@sopel.module.commands('clue')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    channel = trigger.sender
    target = get_trigger_arg(triggerargsarray, 1)
    suspect = get_trigger_arg(triggerargsarray, 2)
    players = []
    for u in bot.channels[channel].users:
        disenable = get_botdatabase_value(bot, u, 'disenable')
        if disenable:
            players.append(u)
    random.shuffle(rooms)
    random.shuffle(weapons)
    random.shuffle(players)
    if rooms[0] == 'secret passage':
        bot.say(players[2] + " evaded " + players[0] + " by using the secret passage. So " + players[0] + " killed " + players[1] + " with the " + weapons[0] + " instead.")    
    else:
        bot.say(players[0] + " killed " + players[1] + " in the " + rooms[0] + " with the " + weapons[0] + ".")
    import Points
    if target:
        if suspect:
            if suspect == 'killer' and target == players[0]:
                bot.say('You guessed the killer correctly!')
                Points.pointstask(bot, channel, 'SpiceBot', trigger.nick, ' gives ', ' to', 'up', 'points', trigger.sender)
            elif suspect == 'killed' and target == players[1]:
                bot.say('You guessed the person murdered!')
                Points.pointstask(bot, channel, 'SpiceBot', trigger.nick, ' gives ', ' to', 'up', 'points', trigger.sender)
    elif target and target == players[0]:
        bot.say('You guessed the killer correctly!')
        Points.pointstask(bot, channel, 'SpiceBot', trigger.nick, ' gives ', ' to', 'up', 'points', trigger.sender)
    if players[0] == trigger.nick:
        bot.say('You were the killer.')
        Points.pointstask(bot, channel, 'SpiceBot', trigger.nick, ' takes ', ' from', 'down', 'points', trigger.sender)
