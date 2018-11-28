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
# import Spicebucks
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('decktest')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'decktest')
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, arg):
    myscore = 0
    myhand = spicemanip(bot, arg, '1+') or 'A'
    if len(myhand) >= 12:
        osd(bot, trigger.sender, 'say', "Player wins for having more then 6 cards.")
    else:
        # myhand =spicemanip(bot,myhand,'list')
        osd(bot, trigger.sender, 'say', "Input: " + str(myhand))
        myscore = blackjackscore(bot, myhand)
    osd(bot, trigger.sender, 'say', "Player score is: " + str(myscore))
    reset_database_value(bot, 'casino', 'deckscorecount')


def blackjackscore(bot, hand):
    myscore = 0
    myhand = []

    handlen = len(hand)
    # counter = get_database_value(bot,'casino','deckscorecount')
    #

    for i in range(0, handlen):
        card = spicemanip(bot, hand, i)
        if card.isdigit():
            myscore = myscore+int(card)
        elif(card == 'J' or card == 'Q' or card == 'K'):
            myscore = myscore + 10
        elif card == 'A':
            myscore = myscore + 11
    if myscore > 21:
        # counter = get_database_value(bot,'casino','deckscorecount')
        # if counter >5:
            # return myscore
        if 'A' in hand:
            myhand = hand.replace('A', '1')
            # adjust_database_value(bot, 'casino', 'deckscorecount',1)
            newscore = blackjackscore(bot, myhand)
            return newscore
        else:
            return myscore
    else:
        return myscore


def blackjackreset(bot, player):
    reset_database_value(bot, player, 'myhand')
    reset_database_value(bot, player, 'dealerhand')
    reset_database_value(bot, player, 'mybet')
