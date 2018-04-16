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
    card1 = get_trigger_arg(bot, arg, 1) or 'A'
    card2 = get_trigger_arg(bot,arg,2) or 'J'
    card3 = get_trigger_arg(bot,arg,3) or ''
    card4 = get_trigger_arg(bot,arg,4) or ''
    card5=get_trigger_arg(bot,arg,5) or ''
    myhand = card1+' '+card2+' '+card3+' '+ card4
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
        hand =get_trigger_arg(bot,hand,'list')
        hand=hand.replace('A','1')
        blackjackscore(bot,hand)     
    return myscore

def blackjackreset(bot,player):   
    reset_botdatabase_value(bot,player, 'myhand')
    reset_botdatabase_value(bot,player, 'dealerhand')
    reset_botdatabase_value(bot,player, 'mybet')
