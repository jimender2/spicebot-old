#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import arrow
import sys
import os
import datetime
import random
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)

from SpicebotShared import *

@sopel.module.commands('bribedev')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)

def execute_main(bot, trigger, triggerargsarray):
    instigator = trigger.nick
    target = get_trigger_arg(bot, triggerargsarray, 1)
    money = random.randint(1,100001)
    bot.say(instigator + " bribes " + target + " with $" + str(money) + " in nonsequental, unmarked bills.")

    
    
    balance=bank(bot, target)

    
    botusersarray = get_botdatabase_value(bot, bot.nick, 'botusers') or []
    channel = trigger.sender
    botuseron=[]
    for u in bot.users:
        if u in botusersarray and u != bot.nick:
            botuseron.append(u)
            
def bank(bot, nick):
    balance = get_botdatabase_value(bot,nick,'spicebucks_bank') or 0
    return balance

def spicebucks(bot, target, plusminus, amount):
    #command for getting and adding money to account
    success = 'false'
    if type(amount) == int:
        inbank = bank(bot,target)
    if plusminus == 'plus':
       adjust_botdatabase_value(bot,target, 'spicebucks_bank', amount)
       success = 'true'
    elif plusminus == 'minus':
        if inbank - amount < 0:
            #bot.say("I'm sorry, you do not have enough spicebucks in the bank to complete this transaction.")
            success = 'false'
        else:
            adjust_botdatabase_value(bot,target, 'spicebucks_bank', -amount)
            success = 'true'
    else:
        #bot.say("The amount you entered does not appear to be a number.  Transaction failed.")
        success = 'false'
    return success #returns simple true or false so modules can check the if tranaction was a success
