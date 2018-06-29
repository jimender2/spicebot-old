#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

#author jimender2

@sopel.module.commands('shame')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'shame')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)

def execute_main(bot, trigger, triggerargsarray):
    botusersarray = get_botdatabase_value(bot, bot.nick, 'botusers') or []
    channel = trigger.sender
    commandused = get_trigger_arg(bot, triggerargsarray, 1) or 'nocommand'
    botuseron=[]
    for u in bot.users:
        if u in botusersarray and u != bot.nick:
            botuseron.append(u)

    if commandused == 'nocommand':
        bot.say("")
    else:
        
#admin command reset user values
def reset(bot, target):
    reset_botdatabase_value(bot,target, '')
    reset_botdatabase_value(bot,target,'')    
    reset_botdatabase_value(bot,target,'')

def timesShamed(bot, nick):
    balance = get_botdatabase_value(bot,nick,'') or 0
    return balance

def shame(bot, target, plusminus, amount):
    #command for getting and adding money to account
    success = 'false'
    if type(amount) == int:
        inbank = bank(bot,target)
    if plusminus == 'plus':
       adjust_botdatabase_value(bot,target, '', amount)
       success = 'true'
    elif plusminus == 'minus':
        if inbank - amount < 0:
            success = 'false'
        else:
            adjust_botdatabase_value(bot,target, 'spicebucks_bank', -amount)
            success = 'true'
    else:
        success = 'false'
    return success

def checkpayday(bot, target):
    paydayamount=0
    now = datetime.datetime.now()
    datetoday = int(now.strftime("%Y%j"))
    spicebank = bank(bot,'SpiceBank')
    lastpayday = get_botdatabase_value(bot,target, 'spicebucks_payday') or 0
    if lastpayday == 0 or lastpayday < datetoday:
        paydayamount = int(spicebank * 0.01)
        set_botdatabase_value(bot,target, 'spicebucks_payday', datetoday)
    else:
        paydayamount=0
    return paydayamount

def paytaxes(bot, target):
    now = datetime.datetime.now()
    datetoday = int(now.strftime("%Y%j"))
    lasttaxday = get_botdatabase_value(bot,target, 'spicebucks_taxday') or 0
    inbank = bank(bot,target) or 0    
    taxtotal = 0
    if lasttaxday == 0 or lasttaxday < datetoday:
        reset_botdatabase_value(bot,target,'usedtaxes')
        taxtotal = int(inbank * .1)
        if inbank == 1:
            taxtotal = 1
        if taxtotal>0:
            spicebucks(bot, 'SpiceBank', 'plus', taxtotal)
            spicebucks(bot, target, 'minus', taxtotal)
            set_botdatabase_value(bot,target, 'spicebucks_taxday', datetoday)
            bot.say("Thank you for reminding me that " + target + " has not paid their taxes today. " + str(taxtotal) + " spicebucks will be transfered to the SpiceBank.")
            return taxtotal            
        else:
            bot.say(target + ' is broke and cannot pay taxes today')
            return taxtotal
    else:
        bot.say("Taxes already paid today.")
        return taxtotal
    

def transfer(bot, instigator, target, amount):
    validamount = 0
    if amount>=0:
        if spicebucks(bot, instigator, 'minus', amount) == 'true':
            spicebucks(bot, target, 'plus', amount)
            validamount = 1
    return validamount
