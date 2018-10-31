#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
from random import random
from random import randint
moduledir = os.path.dirname(os.path.dirname(__file__))
gamesdir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Games")
sys.path.append(gamesdir)
sys.path.append(moduledir)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *
from Bucks import *

monopolyfee = 5

gooddeck = ["an 'Advance to Go' card", "a 'Bank error in your favor' card", "a 'Your crypto miner pays off' card"]
baddeck = ["a 'Pay poor tax' card", "a 'Hit with ransomware' card", "a 'License audit fails' card"]
neutraldeck = ["a 'Get out of Jail Free' card", "a 'Go directly to Jail, Do not pass Go, Do not collect 200 dollars' card", "a 'Go Back 3 Spaces' card"]


@sopel.module.commands('monopoly', 'chance')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'monopoly')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    channel = trigger.sender
    instigator = trigger.nick
    deckchoice = randint(1, 3)
    payment = random.uniform(0.1, 0.3)
    balance = bank(bot, botcom, instigator)
    payout = int(payment*balance)

    if transfer(bot, botcom, instigator, 'casino', monopolyfee):
        if deckchoice == 1:
            chancecard = spicemanip(bot, gooddeck, 'random')
            msg = chancecard + " and wins " + str(payout) + " Spicebucks"
            addbucks(bot, botcom, instigator, payout)
        elif deckchoice == 2:
            chancecard = spicemanip(bot, baddeck, 'random')
            msg = chancecard + " and loses " + str(payout) + " Spicebucks"
            minusbucks(bot, botcom, instigator, payout)
        elif deckchoice == 3:
            msg = spicemanip(bot, neutraldeck, 'random')
            payout = 0
        osd(bot, channel, 'say', instigator + " risks " + str(monopolyfee) + " Spicebucks to draw a card from the chance deck! " + instigator + " gets " + msg + ".")
    else:
        osd(bot, instigator, 'priv', "You need " + str(monopolyfee) + " Spicebucks to use this command.")
