#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import datetime
from sopel import module, tools
import sys
import os
import random
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

 
@sopel.module.commands('spicebucks')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, args):
    botusersarray = bot.users or []
    #for c in bot.channels:
        #channel = c
    #commandused = trigger.group(3)
    #inchannel = trigger.sender
    commandused = get_trigger_arg(triggerargsarray, 1) or 'nocommand'
	
    if commandused == nocommand:
        bot.say("Welcome to the #Spiceworks Bank.  Your options are payday, transfer and bank.")
    else:
    ##PayDay
	if commandused == 'payday':
		paydayamount = 0
		paydayamount=checkpayday(bot, trigger.nick)
		if paydayamount > 0:
			spicebucks(bot, trigger.nick, 'plus', paydayamount)
			bot.say("You haven't been paid yet today. Here's your " + str(paydayamount) + " spicebucks.")
		else:
			bot.say("You've already been paid today. Now go do some work.")
    ####MakeitRain
	elif commandused == 'makeitrain':		
		target = get_trigger_arg(triggerargsarray, 2) or 'notarget'
		if (target == 'notarget' or target == 'random'):
			target = randomuser(bot,trigger.nick)
			if target == 'None':
				target = randomuser(bot,trigger.nick)				
				bankbalance = bank(bot,trigger.nick)
				if bankbalance <=0:
					spicebucks(bot, trigger.nick, 'plus', 15)
					bankbalance = 15
					maxpayout = bankbalance			
	    		bot.say(trigger.nick + ' rains Spicebucks down on ' + target)
				winnings=random.randint(1,maxpayout)
				transfer(bot, trigger.nick, target, winnings)
				bot.say(target + " manages to keep " + str(winnings) + " of " + trigger.nick + "'s spicebucks.")					
			elif not target.lower() in [u.lower() for u in bot.users]:
				bot.say("I'm sorry, I do not know who " + target + " is.")
			else:
				
				bankbalance = bank(bot,trigger.nick)
				if bankbalance <=0:
					spicebucks(bot, trigger.nick, 'plus', 15)
					bankbalance = 15
				maxpayout = bankbalance
				bot.action('rains Spicebucks on ' + target)
				winnings=random.randint(1,maxpayout)
				bot.say(target + " manages to keep " + str(winnings) + " of " + trigger.nick + "'s spicebucks")
				transfer(bot, trigger.nick, target, winnings)											
    ##Reset
	elif commandused == 'reset' and trigger.admin: #admin only command
		target = get_trigger_arg(triggerargsarray, 2) or 'notarget'
		if not target == 'notarget':				
			if not target.lower() in [u.lower() for u in bot.users]:
				bot.say("I'm sorry, I do not know who " + target + " is.")
			else:
				reset(bot,target)
				bot.say('Payday reset for ' + target)					
		else:
			reset(bot,trigger.nick)
			bot.say('Payday reset for ' + trigger.nick)
			
    ##Funds
	elif commandused == 'funds' and trigger.admin: #admin only command
		success = 0
		target = get_trigger_arg(triggerargsarray, 2) or 'notarget'
		if not target == 'notarget'
			if target.lower() == 'spicebank': 				
				target = 'SpiceBank'
				success = 1
			elif not target.lower() in [u.lower() for u in bot.users]:
				bot.say("I'm sorry, I do not know who " + target + " is.")
				success = 0
			else:
				success = 1
				
			if success == 1:
				amount =get_trigger_arg(triggerargsarray, 3) or 'noamount'
				if not amount =='noamount':
					if amount.isdigit():
						amount = int(amount)
						if amount>=0 and amount <10000001:
							bot.db.set_nick_value(target, 'spicebucks_bank', amount)
							targetbalance = bank(bot,target)
							bot.say(target + ' now has ' + str(targetbalance) + ' in the bank')					
						else:
							bot.say('Please enter a postive number less then 1,000,000')
				else:
					bot.say('Please enter a valid a amount to set the bank account to')
		else:
			bot.say('Please enter a target and an amount to set their bank balance at')					
    ##Taxes
	elif (commandused == 'taxes' or commandused == 'tax'):
		target = get_trigger_arg(triggerargsarray, 2) or 'notarget'
		if not target == 'notarget':
			 if not target.lower() in [u.lower() for u in bot.users]:
				bot.say("I'm sorry, I do not know who " + target + " is.")					
			else:
				paytaxes(bot, target)
		else:
			paytaxes(bot, trigger.nick)
    ##Bank
	elif commandused == 'bank':
		target = get_trigger_arg(triggerargsarray, 2) or 'notarget'
		if not target == 'notarget':
			if target == 'spicebank':
				balance = bot.db.get_nick_value('SpiceBank', 'spicebucks_bank') or 0
				bot.say('The current casino jackpot is ' + str(balance))
				
			elif if not target.lower() in [u.lower() for u in bot.users]:
				bot.say("I'm sorry, I do not know who " + target + " is.")				
			else:
				balance=bank(bot, target)                                         
				bot.say(target + ' has '+ str(balance) + " spicebucks in the bank.")
		else:
			balance=bank(bot, trigger.nick)
			bot.say("You have " + str(balance) + " spicebucks in the bank.")       
    ##Transfer
	elif commandused == 'transfer':
		target = get_trigger_arg(triggerargsarray, 2) or 'notarget'
		amount =get_trigger_arg(triggerargsarray, 3) or 'noamount'
		if not (target=='notarget' or amount=='noamount'):				
			instigator = trigger.nick				
			if not amount.isdigit():
				bot.say('Please enter the person you wish to transfer to followed by an amount you wish to transfer')
			else:	
				amount=int(amount)		
				if not target.lower() in [u.lower() for u in bot.users]:
					bot.say("I'm sorry, I do not know who you want to transfer money to.")
				else:
					if target == instigator:
						bot.say("You cannot transfer spicebucks to yourself!")
					else:
						if amount <=0:								
							bot.say(instigator + " gave no spicefucks about " + target + "'s comment.")
						else:
							balance=bank(bot, instigator)
							if amount <= balance:
								success = transfer(bot,  instigator, target, amount)
								if success == 1:
									bot.say(instigator + " successfully transfered " + str(amount) + " spicebucks to " + target + ".") 
								else:
									bot.say('The transfer was unsuccesfully check the amount and try again')
							else:
								bot.say('Insufficient funds to transfer')
			else:
    			bot.say("You must enter who you would like to transfer spicebucks to, as well as an amount.")
           
def reset(bot, target): #admin command reset user values
    bot.db.set_nick_value(target, 'spicebucks_payday', 0)
    bot.db.set_nick_value(target, 'spicebucks_taxday', 0)
	
    
def bank(bot, nick):
    balance = bot.db.get_nick_value(nick, 'spicebucks_bank') or 0
    return balance

def spicebucks(bot, target, plusminus, amount):
	#command for getting and adding money to account
    success = 'false'
    if type(amount) == int:
        inbank = bot.db.get_nick_value(target, 'spicebucks_bank') or 0
        if plusminus == 'plus':
			bot.db.set_nick_value(target, 'spicebucks_bank', inbank + amount)
			success = 'true'
        elif plusminus == 'minus':
            if inbank - amount < 0:
                #bot.say("I'm sorry, you do not have enough spicebucks in the bank to complete this transaction.")
                success = 'false'
            else:
                bot.db.set_nick_value(target, 'spicebucks_bank', inbank - amount)
                success = 'true'            
    else:
        #bot.say("The amount you entered does not appear to be a number.  Transaction failed.")
        success = 'false'
    return success #returns simple true or false so modules can check the if tranaction was a success
    
    
def checkpayday(bot, target):
	paydayamount=0
	now = datetime.datetime.now()
	datetoday = int(now.strftime("%Y%j"))
	lastpayday = bot.db.get_nick_value(target, 'spicebucks_payday') or 0
	if lastpayday == 0 or lastpayday < datetoday:
		paydayamount = 15
		bot.db.set_nick_value(target, 'spicebucks_payday', datetoday)
	else: 		
		paydayamount=0
	return paydayamount

def paytaxes(bot, target):
	now = datetime.datetime.now()
	datetoday = int(now.strftime("%Y%j"))
	lasttaxday = bot.db.get_nick_value(target, 'spicebucks_taxday') or 0
	inbank = bot.db.get_nick_value(target, 'spicebucks_bank') or 0
	if lasttaxday == 0 or lasttaxday < datetoday:
		taxtotal = int(inbank * .1)
		if inbank == 1:
			taxtotal = 1			
		if taxtotal>0:
			spicebucks(bot, 'SpiceBank', 'plus', taxtotal)
			spicebucks(bot, target, 'minus', taxtotal)
			bot.db.set_nick_value(target, 'spicebucks_taxday', datetoday)
			bot.say("Thank you for reminding me that " + target + " has not paid their taxes today. " + str(taxtotal) + " spicebucks will be transfered to the SpiceBank.")
		else:
			bot.say(target + ' is broke and cannot pay taxes today')
	else:
		bot.say("Taxes already paid today.")   

def transfer(bot, instigator, target, amount):
	validamount = 0
	if amount>=0:
		if spicebucks(bot, instigator, 'minus', amount) == 'true':
			spicebucks(bot, target, 'plus', amount)
			validamount = 1
	return validamount

def randomuser(bot,nick):
	randompersons = []
	for u in bot.users:
		if not(u==nick or u==bot.nick):
			randompersons.append(u)
			randomperson = get_trigger_arg(randompersons,'random')
		else:
			randomperson ='None'
			
	return randomperson
	
