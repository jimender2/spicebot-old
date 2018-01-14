#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
import random
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from Points import *
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
    instigator = trigger.nick
    if not channel.startswith("#"):
        bot.notice(instigator + " Clue must be in a channel.", instigator)
        return
    target = get_trigger_arg(triggerargsarray, 1)
    suspect = get_trigger_arg(triggerargsarray, 2)
    players = []
    botusersarray = get_botdatabase_value(bot, bot.nick, 'botusers') or []
    for u in bot.users:
        if u in botusersarray and u != bot.nick:
            players.append(u) 
    random.shuffle(rooms)
    random.shuffle(weapons)
    random.shuffle(players)
    if rooms[0] == 'secret passage':
        bot.say(players[2] + " evaded " + players[0] + " by using the secret passage. So " + players[0] + " killed " + players[1] + " with the " + weapons[0] + " instead.")    
    else:
        bot.say(players[0] + " killed " + players[1] + " in the " + rooms[0] + " with the " + weapons[0] + ".")
    if target:
        if suspect:
            if suspect == 'killer' and target == players[0]:
                bot.say('You guessed the killer correctly!')
                bot.say(bot.nick + ' gives 40 points to ' + instigator)
                addpoints(bot, instigator, '40')
                #Points.pointstask(bot, channel, 'SpiceBot', trigger.nick, ' gives ', ' to', 'up', 'points', trigger.sender)
            elif suspect == 'killed' and target == players[1]:
                bot.say('You guessed the person murdered!')
                bot.say(bot.nick + ' gives 40 points to ' + instigator)
                addpoints(bot,instigator,'40')
                #Points.pointstask(bot, channel, 'SpiceBot', trigger.nick, ' gives ', ' to', 'up', 'points', trigger.sender)
    elif target and target == players[0]:
        bot.say('You guessed the killer correctly!')
        bot.say(bot.nick + ' gives 40 points to ' + instigator)
        addpoints(bot,instigator,'40')
        #Points.pointstask(bot, channel, 'SpiceBot', trigger.nick, ' gives ', ' to', 'up', 'points', trigger.sender)
    if players[0] == trigger.nick:
        bot.say('You were the killer.')
        bot.say(bot.nick + ' takes 40 points to ' + instigator)
        takepoints(bot,instigator,'40)
        #Points.pointstask(bot, channel, 'SpiceBot', trigger.nick, ' takes ', ' from', 'down', 'points', trigger.sender)
