#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
from random import random
from random import randint
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *
import Spicebucks

cluefee=5 #amount charged to use the command
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
    pointsworth = random.uniform(.03,.08)   
    if not channel.startswith("#"):
        bot.notice(instigator + " Clue must be in a channel.", instigator)
        return
    target = get_trigger_arg(bot, triggerargsarray, 1)
    suspect = get_trigger_arg(bot, triggerargsarray, 2)
    cluefee=5
    if not target:
        cluefee=0
        pointsworth=0 
    players = []
    if Spicebucks.transfer(bot, trigger.nick, 'SpiceBank', cluefee) == 1:
        bankbalance=Spicebucks.bank(bot,instigator)
        pointsworth = (int(pointsworth*bankbalance)) + 5
        pointsvalue = str(pointsworth)
        bot.say(trigger.nick + " paid " + str(cluefee) + " spicebucks and started a game of clue.")
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
                    bot.say(bot.nick + ' gives ' + pointsvalue + ' Spicebucks to ' + instigator)
                    Points.addpoints(bot, instigator, pointsworth)
                elif suspect == 'killed' and target == players[1]:
                    bot.say('You guessed the person murdered!')
                    bot.say(bot.nick + ' gives ' + pointsvalue + 'Spicebucks to ' + instigator)
                    Spicebucks.spicebucks(bot,instigator,'plus',pointsworth)
        elif target and target == players[0]:
            bot.say('You guessed the killer correctly!')
            bot.say(bot.nick + ' gives ' + pointsvalue + ' Spicebucks to' + instigator)
            Spicebucks.spicebucks(bot,instigator,'plus',pointsworth)
        if players[0] == trigger.nick:
            bot.say('You were the killer.')      
            
            if pointsworth>bankbalance:
                pointsworth=bankbalance
            Spicebucks.spicebucks(bot,instigator,'minus',pointsworth)
            bot.say(bot.nick + ' takes ' + pointsvalue + ' Spicebucks from ' + instigator)
    else:
        bot.notice("You need " + str(cluefee) + " spicebucks to use this command.",instigator) 
        
