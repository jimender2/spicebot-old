#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel.module

# imports for system and OS access, directories
import os
import sys

# imports based on THIS file
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# Ensure Encoding
reload(sys)
sys.setdefaultencoding('utf-8')


@sopel.module.commands('decktest')
def mainfunction(bot, trigger):

    botcom = bot_module_prerun(bot, trigger)
    if not botcom.modulerun:
        return
    # IF "&&" is in the full input, it is treated as multiple commands, and is split
    commands_array = spicemanip(bot, botcom.triggerargsarray, "split_&&")
    if commands_array == []:
        commands_array = [[]]
    for command_split_partial in commands_array:
        botcom.triggerargsarray = spicemanip(bot, command_split_partial, 'create')
        execute_main(bot, trigger, botcom)


def execute_main(bot, trigger, botcom):
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
