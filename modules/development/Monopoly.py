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

monopolyfee = 5

chancedeck = ['Advance to Go and Collect 20','Bank error in your favor collect 10 spicebucks','Your crypto miner pays off—Collect 20',
              'Pay poor tax of 15','Hit with ransomware, pay 20 spicebucks','Get out of Jail Free','Go to Jail–Go directly to Jail–Do not pass Go, do not collect $200']

@sopel.module.commands('monopoly','change')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, 'monopoly')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    channel = trigger.sender
    instigator = trigger.nick
    chancecard=get_trigger_arg(bot,chancedeck,random)
    bot.say(instigator + " risks " + str(monopolyfee) +" draws a card from the chance deck and gets " + chancecard)
