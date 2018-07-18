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


@sopel.module.commands('spicebucks','bank','payday','tax','taxes','funds')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger,'spicebucks')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    botusersarray = get_database_value(bot, bot.nick, 'botusers') or []
    channel = trigger.sender
    commandused = trigger.group(1) or 'nocommand'
    target = get_trigger_arg(bot, triggerargsarray, 1) or 'notarget'
    player = instigator.default

    if commandused == 'nocommand':
        message = "Welcome to the SpiceBank.  Your options are payday, tax, makeitrain, and bank."
        onscreentext(bot, ['say'],message)
    elif commandused == 'payday':
        paydayamount = 0
        paydayamount = checkpayday(bot, player)
        if paydayamount > 0:
            spicebucks(bot, player, 'plus', paydayamount)
            message = "You haven't been paid yet today. Here's your " + str(paydayamount) + " spicebucks."
            onscreentext(bot, ['say'],message)
        else:
            message = player + ", you've already been paid today. Now go do some work."
            onscreentext(bot, ['say'],message)
    elif commandused == 'funds' and trigger.admin:  # admin only command
        success = 0
        target = get_trigger_arg(bot, triggerargsarray, 2) or 'notarget'
        if not target == 'notarget':
            if target.lower() == 'spicebank':
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
                        targetbalance = bank(bot,target)
                        osd(bot, trigger.sender, 'say', target + ' now has ' + str(targetbalance) + ' in the bank')
                    else:
                        osd(bot, trigger.sender, 'say', 'Please enter a postive number less then 1,000,000')
                else:
                    osd(bot, trigger.sender, 'say', 'Please enter a valid a amount to set the bank balance to')
            else:
                osd(bot, trigger.sender, 'say', 'Please enter a target and an amount to set their bank balance at')

        # Taxes
        elif (commandused == 'taxes' or commandused == 'tax'):
            if not channel.startswith("#"):
                bot.notice(player + ", " + commandused + " can only be used in a channel.", player)
            else:
                target = get_trigger_arg(bot, triggerargsarray, 2) or 'notarget'
                if not target == 'notarget':
                    if targetcheck(bot,target,player) == 0:
                        osd(bot, trigger.sender, 'say', "I'm sorry, I do not know who " + target + " is.")
                    elif targetcheck(bot,target,player) == 2:
                        inbank = bank(bot,player)
                        auditamount = int(inbank * .20)
                        if auditamount > 0:
                            bot.action("carries out an audit on " + player + " and takes " + str(auditamount) + " spicebucks for the pleasure.")
                            spicebucks(bot,player,'minus',auditamount)

                        else:
                            bot.action("carries out an audit on " + player + " but finds no spicebucks to take.")
                            reset_database_value(bot,target,'usedtaxes')
                    else:
                        if get_database_value(bot,player,'usedtaxes') < 2:
                            adjust_database_value(bot,player,'usedtaxes',1)
                            taxtotal = paytaxes(bot, target)
                            if taxtotal >= 100:
                                kickback = int(taxtotal*0.1)
                                adjust_database_value(bot,player,'spicebucks_bank',kickback)
                                bot.action("gives " + player + " a kickback of " + str(kickback) + " for bringing this delinquent to our attention")
                        else:
                            inbank = bank(bot,player)
                            auditamount = int(inbank * .20)
                            if auditamount > 0:
                                bot.action("carries out an audit on " + player + " and takes " + str(auditamount) + " spicebucks for the pleasure.")
                                spicebucks(bot,player,'minus',auditamount)

                            else:
                                bot.action("carries out an audit on " + player + " but finds no spicebucks to take.")
                                reset_database_value(bot,target,'usedtaxes')
                else:
                    adjust_database_value(bot,player,'usedtaxes',1)
                    taxtotal = paytaxes(bot, player)

        elif commandused == 'rob':
            target = get_trigger_arg(bot, triggerargsarray, 2) or 'notarget'
            balance = bank(bot, target)
            if targetcheck(bot,target,player) == 0:
                osd(bot, trigger.sender, 'say', "I'm sorry, I do not know who " + target + " is.")
            else:
                if get_database_value(bot,player,'usedtaxes') > 2:
                    adjust_database_value(bot,player,'usedtaxes',1)
                    triggerbalance = bank(bot, player)
                    fine = int(triggerbalance*.20)
                    osd(bot, trigger.sender, 'say', player + " get's caught for pickpocketing too much and is fined " + str(fine))
                    spicebucks(bot,player,'minus',fine)
                else:
                    adjust_database_value(bot,player,'usedtaxes',1)
                    randomcheck = random.randint(0,5)
                    if randomcheck == 3:
                        triggerbalance = bank(bot, player)
                        fine = int(triggerbalance*.20)
                        osd(bot, trigger.sender, 'say', player + " get's caught trying to pickpocket " + target + " and is fined for " + str(fine))
                        spicebucks(bot,player,'minus',fine)
                    else:
                        payout = int(balance * .01)
                        osd(bot, trigger.sender, 'say', player + " pickpockets " + str(payout) + " from " + target)

                        transfer(bot,target,player,payout)
        # Bank
        elif commandused == 'bank':
            target = get_trigger_arg(bot, triggerargsarray, 2) or 'notarget'
            checkedtarget = targetcheck(bot,target,player) or 0

            if not target == 'notarget':
                if target == 'spicebank':
                    balance = bank(bot,'spicebucks') or 0
                    osd(bot, trigger.sender, 'say', 'The current casino jackpot is ' + str(balance))
                elif checkedtarget == 0:
                    osd(bot, trigger.sender, 'say', "I'm sorry, I do not know who " + target + " is.")
                else:
                    balance = bank(bot, target)
                    osd(bot, trigger.sender, 'say', target + ' has ' + str(balance) + " spicebucks in the bank.")
            else:
                balance = bank(bot, player)
                osd(bot, trigger.sender, 'say', "You have " + str(balance) + " spicebucks in the bank.")


# admin command reset user values
def reset(bot, target):
    reset_database_value(bot,target, 'spicebucks_payday')
    reset_database_value(bot,target,'spicebucks_taxday')
    reset_database_value(bot,target,'usedtaxes')


def bank(bot, nick):
    balance = get_database_value(bot,nick,'spicebucks_bank') or 0
    return balance


def spicebucks(bot, target, plusminus, amount):
    # command for getting and adding money to account
    success = 'false'
    if type(amount) == int:
        inbank = bank(bot,target)
    if plusminus == 'plus':
        adjust_database_value(bot,target, 'spicebucks_bank', amount)
        success = 'true'
    elif plusminus == 'minus':
        if inbank - amount < 0:
            # osd(bot, trigger.sender, 'say', "I'm sorry, you do not have enough spicebucks in the bank to complete this transaction.")
            success = 'false'
        else:
            adjust_database_value(bot,target, 'spicebucks_bank', -amount)
            success = 'true'
    else:
        # osd(bot, trigger.sender, 'say', "The amount you entered does not appear to be a number.  Transaction failed.")
        success = 'false'
    return success  # returns simple true or false so modules can check the if tranaction was a success


def checkpayday(bot, target):
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


def paytaxes(bot, target):
    now = datetime.datetime.now()
    datetoday = int(now.strftime("%Y%j"))
    lasttaxday = get_database_value(bot,target, 'spicebucks_taxday') or 0
    inbank = bank(bot,target) or 0
    taxtotal = 0
    if lasttaxday == 0 or lasttaxday < datetoday:
        reset_database_value(bot,target,'usedtaxes')
        taxtotal = int(inbank * .1)
        if inbank == 1:
            taxtotal = 1
        if taxtotal > 0:
            spicebucks(bot, 'SpiceBank', 'plus', taxtotal)
            spicebucks(bot, target, 'minus', taxtotal)
            set_database_value(bot,target, 'spicebucks_taxday', datetoday)
            osd(bot, trigger.sender, 'say', "Thank you for reminding me that " + target + " has not paid their taxes today. " + str(taxtotal) + " spicebucks will be transfered to the SpiceBank.")
            return taxtotal
        else:
            osd(bot, trigger.sender, 'say', target + ' is broke and cannot pay taxes today')
            return taxtotal
    else:
        osd(bot, trigger.sender, 'say', "Taxes already paid today.")
        return taxtotal


def transfer(bot, instigator, target, amount):
    validamount = 0
    if amount >= 0:
        if spicebucks(bot, instigator, 'minus', amount) == 'true':
            spicebucks(bot, target, 'plus', amount)
            validamount = 1
    return validamount


def randomuser(bot,nick):
    randompersons = []
    randomperson = ''
    botusersarray = get_database_value(bot, bot.nick, 'botusers') or []
    for u in bot.users:
        if u in botusersarray and u != bot.nick and u != nick:
            randompersons.append(u)
    randomperson = get_trigger_arg(bot, randompersons,'random')
    return randomperson
