#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
from sopel import module, tools
import sys
import os
import random
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
import Spicebucks
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *


@sopel.module.commands('decktest')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'decktest')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
        
def execute_main(bot, trigger, arg):
    myscore=0
    myhand = get_trigger_arg(bot, arg, '1+') or 'A'    
    bot.say("Input: "+ myhand)
    myscore= blackjackscore(bot,myhand)
    
    bot.say(str(myscore))
    

def blackjackscore(bot,hand):
    myscore = 0
    for card in hand:
        if(card == 'J' or card == 'Q' or card == 'K'):
            myscore = myscore + 10
        elif card=='A':
            testscore = myscore + 11
            if testscore>21:
                myscore = myscore + 1
            else:
                myscore = myscore + 11
        else:
            try:
                myscore = myscore + int(card)
            except ValueError:
                myscore=myscore
    if myscore >21:
        for x in range(0,(len(hand)-1)):
            if x == 'A':
                hand[x]='1'       
        blackjackscore(bot,hand) 
    bot.say("Scoring hand: " + hand)
    return myscore

def blackjackreset(bot,player):   
    reset_botdatabase_value(bot,player, 'myhand')
    reset_botdatabase_value(bot,player, 'dealerhand')
    reset_botdatabase_value(bot,player, 'mybet')
