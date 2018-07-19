#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import datetime
from sopel import module, tools
import sys
import os
import random
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *
from Bucks import *


@sopel.module.commands('banker','payday','tax','taxes','funds','rob','bankreset')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger,'banker')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    commandused = trigger.group(1)
    target = (get_trigger_arg(bot, triggerargsarray, 1)).lower() or 'notarget'
    player = instigator.default
    bot.say("Command used:" + str(commandused))
    if commandused == '':
        message = "Welcome to the SpiceBank.  Your options are payday, tax, , and bank."
        osd(bot, trigger.sender, 'say', message)
    elif commandused == 'payday':
        paydayamount = 0
        paydayamount = checkpayday(bot,botcom, player)
        if paydayamount > 0:
            addbucks(bot,botcom, player, paydayamount)
            message = "You haven't been paid yet today. Here's your " + str(paydayamount) + " spicebucks."
            osd(bot, trigger.sender, 'say', message)
        else:
            message = player + ", you've already been paid today. Now go do some work."
            osd(bot, trigger.sender, 'say', message)
    elif commandused == 'funds' and trigger.admin:  # admin only command
        success = 0
        if not target == 'notarget':
            if target == 'spicebank':
                target = 'SpiceBank'
                success = 1
            elif targetcheck(bot,botcom,target,instigator) == 0:
                osd(bot, trigger.sender, 'say', "I'm sorry, I do not know who " + target + " is.")
                success = 0
            else:
                success = 1
        if success == 1:
            amount = get_trigger_arg(bot, triggerargsarray, 3) or 'noamount'
            if not amount == 'noamount':
                if amount.isdigit():
                    amount = int(amount)
                    if amount >= 0 and amount < 10000001:
                        set_database_value(bot,target, 'spicebucks_bank', amount)
                        targetbalance = bank(bot,botcom,target)
                        osd(bot, trigger.sender, 'say', target + ' now has ' + str(targetbalance) + ' in the bank')
                    else:
                        osd(bot, trigger.sender, 'say', 'Please enter a postive number less then 1,000,000')
                else:
                    osd(bot, trigger.sender, 'say', 'Please enter a valid a amount to set the bank balance to')
            else:
                osd(bot, trigger.sender, 'say', 'Please enter a target and an amount to set their bank balance at')

        # Taxes
        elif (commandused == 'taxes' or commandused == 'tax'):
            usedamount = (get_database_value(bot,player,'usedtaxes') or 0) + 1
            if not channel.startswith("#"):
                osd(bot, player, 'notice', commandused + " can only be used in a channel.")
            else:
                randomaudit = random.randint(1,usedamount)
                if not target == 'notarget':
                    if targetcheck(bot,botcom,target,player) == 0:
                        osd(bot, trigger.sender, 'say', "I'm sorry, I do not know who " + target + " is.")
                    elif targetcheck(bot,botcom,target,player) == 3:
                        message = audit(bot,botcom,player)
                        osd(bot, trigger.sender, 'action',message)
                    else:
                        if usedamount == 1:
                            adjust_database_value(bot,player,'usedtaxes',3)
                            taxtotal,message = paytaxes(bot, target)
                            osd(bot,trigger.send,'say',message)
                            if taxtotal >= 100:
                                kickback = int(taxtotal*0.1)
                                addbucks(bot,botcom,player,kickback)
                                osd(bot, trigger.sender, 'action', "gives " + player + " a kickback of " + str(kickback) + " for bringing this delinquent to our attention")
                        else:
                            message = audit(bot,botcom,player)
                            osd(bot, trigger.sender, 'action',message)
                else:
                    taxtotal,message = paytaxes(bot, player)
                    osd(bot,trigger.send,'say',message)

        elif commandused == 'rob':
            usedamount = (get_database_value(bot,player,'usedtaxes') or 0) + 2
            balance = bank(bot,botcom, target)
            if targetcheck(bot,botcom,target,player) == 0:
                osd(bot, trigger.sender, 'say', "I'm sorry, I do not know who " + target + " is.")
            else:
                if usedamount > 10:
                    adjust_database_value(bot,player,'usedtaxes',0)
                    triggerbalance = bank(bot, player)
                    fine = int(triggerbalance*.20)
                    osd(bot, trigger.sender, 'say', player + " get's caught for pickpocketing too much and is fined " + str(fine))
                    minusbucks(bot,player,fine)
                else:
                    adjust_database_value(bot,player,'usedtaxes',1)
                    randomcheck = random.randint(0,5)
                    if randomcheck == 3:
                        triggerbalance = bank(bot,botcom, player)
                        fine = int(triggerbalance*.20)
                        osd(bot, trigger.sender, 'say', player + " get's caught trying to pickpocket " + target + " and is fined for " + str(fine))
                        minusbucks(bot,botcom,player,fine)
                    else:
                        payout = int(balance * .01)
                        osd(bot, trigger.sender, 'say', player + " pickpockets " + str(payout) + " from " + target)
                        transfer(bot,botcom,target,player,payout)
        # Bank
    elif commandused == 'banker' or commandused == 'banker':
        if target == 'notarget':
            target = player
            balance = bank(bot,botcom,target)
            osd(bot,trigger.sender, 'say', target + " has " + balance + " in the Spicebank.")

    elif commandused == 'bankreset' and trigger.admin:  # admin only command
        target = get_trigger_arg(bot, triggerargsarray, 2) or 'notarget'
        validtarget = targetcheck(bot,botcom,target,instigator)
        if target == 'notarget'or target == trigger.nick:
            reset(bot,target)
            osd(bot, trigger.sender, 'say', 'Payday reset for ' + trigger.nick)
        elif not validtarget == 1:
            reset(bot,target)
            osd(bot, trigger.sender, 'say', 'Payday reset for ' + target)
        else:
            osd(bot, trigger.sender, 'say', "I'm sorry, I do not know who " + target + " is.")


# admin command reset user values
def reset(bot, target):
    reset_database_value(bot,target, 'spicebucks_payday')
    reset_database_value(bot,target,'spicebucks_taxday')
    reset_database_value(bot,target,'usedtaxes')


def audit(bot,botcom,player):
    inbank = bank(bot,player)
    auditamount = int(inbank * .20)
    msg = ""
    if auditamount > 0:
        msg = "carries out an audit on " + player + " and takes " + str(auditamount) + " spicebucks for the pleasure."
        minusbucks(bot,player,auditamount)
    else:
        msg = "carries out an audit on " + player + " but finds no spicebucks to take."
        reset_database_value(bot,player,'usedtaxes')
    return msg


def checkpayday(bot,botcom, target):
    paydayamount = 0
    now = datetime.datetime.now()
    datetoday = int(now.strftime("%Y%j"))
    spicebank = bank(bot,'SpiceBank')
    lastpayday = get_database_value(bot,target, 'spicebucks_payday') or 0
    if lastpayday == 0 or lastpayday < datetoday:
        paydayamount = int(spicebank * 0.01)
        set_database_value(bot,target, 'spicebucks_payday', datetoday)
    else:
        paydayamount = 0
    return paydayamount


def paytaxes(bot,botcom,target):
    now = datetime.datetime.now()
    datetoday = int(now.strftime("%Y%j"))
    lasttaxday = get_database_value(bot,target, 'spicebucks_taxday') or 0
    inbank = bank(bot,target) or 0
    taxtotal = 0
    message = ""
    if lasttaxday == 0 or lasttaxday < datetoday:
        reset_database_value(bot,target,'usedtaxes')
        taxtotal = int(inbank * .1)
        if inbank == 1:
            taxtotal = 1
        if taxtotal > 0:
            addbucks(bot, 'SpiceBank', taxtotal)
            minusbucks(bot, target, taxtotal)
            set_database_value(bot,target, 'spicebucks_taxday', datetoday)
            message = "Thank you for reminding me that " + target + " has not paid their taxes today. " + str(taxtotal) + " spicebucks will be transfered to the SpiceBank."
        else:
            message = target + " is broke and cannot pay taxes today"
    else:
        message = "Taxes already paid today."
    return taxtotal,message
