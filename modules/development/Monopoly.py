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

gooddeck = ['Advance to Go and Collect ','Bank error in your favor collect ','Your crypto miner pays off, collect ']             
baddeck = ['Pay poor tax of ','Hit with ransomware, pay ','Licenese audit fails, pay ']
neturaldeck =['Get out of Jail Free','Go to Jail–Go directly to Jail–Do not pass Go, do not collect $200','Go Back 3 Spaces']

@sopel.module.commands('monopoly','chance')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, 'monopoly')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    channel = trigger.sender
    instigator = trigger.nick
    deckchoice = randint(1,3)
    payout = randint(10,50)
    if deckchoice == 1:
      chancecard=get_trigger_arg(bot,gooddeck,random)
      msg = chancecard + " and wins " + str(payout) +  " spicebucks"
    elif deckchoice==2:
      chancecard=get_trigger_arg(bot,baddeck,random)      
      msg = chancecard + " and loses " + str(payout) +  " spicebucks"
      payout=-payout    
    elif deckchoice==3:
      msg=get_trigger_arg(bot,neturaldeck,random)
      payout = 0
    bot.say(instigator + " risks " + str(monopolyfee) +" draws a card from the chance deck and gets " + msg)
    balance=bank(bot,instigator)
    if (balance + payout)<0:
      payout = balance
    adjust_botdatabase_value(bot,instigator, 'spicebucks_bank', payout)
    
