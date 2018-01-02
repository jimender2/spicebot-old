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
    botownerarray, operatorarray, voicearray, adminsarray, allusersinroomarray = special_users(bot)
    #for c in bot.channels:
        #channel = c
    #commandused = trigger.group(3)
    #inchannel = trigger.sender
    if len(args) == 0:
        bot.say("Welcome to the #Spiceworks Bank.  Your options are payday and bank.")
    elif len(args) >= 1:
		if args[0] == 'payday':
			paydayamount = 0
			paydayamount=checkpayday(bot, trigger.nick, args[0])
			if paydayamount > 0:
				spicebucks(bot, trigger.nick, 'plus', paydayamount)
				bot.say("You haven't been paid yet today. Here's your " + str(paydayamount) + " spicebucks.")
			else:
				bot.say("You've already been paid today. Now go do some work.")
			
		elif args[0] == 'makeitrain':
	 		if len(args) > 1:
				if args[1] not in allusersinroomarray:
					bot.say("I'm sorry, I do not know who " + args[1] + " is.")
				else:
					bot.say('Spicebucks rain on ' + args[1])
					winnings=random.randint(1,25)
					bot.say(args[1] + ' manages to keep ' + str(winnings) + ' spicebucks before they disappear.')
					spicebucks(bot, args[1], 'plus', winnings)
		
			else:
				bot.say('Spicebucks rain on down on everyone and disappear')
		
		elif args[0] == 'reset': #admin only command
			if trigger.nick not in adminsarray:
				bot.say('You must be an admin to use this command')
			else:
				if len(args) > 1:
					if args[1] == 'spicebank':
						spicebalance = bot.db.get_nick_value('SpiceBank', 'spicebucks_bank') or 0
						spicebucks(bot, 'SpiceBank', 'minus', spicebalance)
						balance = bot.db.get_nick_value('SpiceBank', 'spicebucks_bank') or 0
						bot.say('The spice bank has been robbed and has ' + str(balance) + ' left')
					elif args[1] not in allusersinroomarray:
						bot.say("I'm sorry, I do not know who " + args[1] + " is.")
					else:
						reset(bot,args[1])
						bot.say('Payday reset for ' + args[1])					
				else:
					reset(bot,trigger.nick)
					bot.say('Payday reset for ' + trigger.nick)		
					
                        
                
		elif args[0] == 'taxes':
			if len(args) > 1:
				if args[1] not in allusersinroomarray:
					bot.say("I'm sorry, I do not know who " + args[1] + " is.")
				else:
					paytaxes(bot, args[1])
			else:
				paytaxes(bot, trigger.nick)
		elif args[0] == 'bank':
			if len(args) > 1:
				if args[1] == 'spicebank':
					balance = bot.db.get_nick_value('SpiceBank', 'spicebucks_bank') or 0
					bot.say('There are ' + str(balance) + ' spicebucks in the Spicebank.')
				elif args[1] not in allusersinroomarray:
					bot.say("I'm sorry, I do not know who " + args[1] + " is.")				
				else:
					balance=bank(bot, args[1])                                         
					bot.say(args[1] + ' has '+ str(balance) + " spicebucks in the bank.")
			else:
				balance=bank(bot, trigger.nick)
				bot.say("You have " + str(balance) + " spicebucks in the bank.")       
                     
		elif args[0] == 'transfer':
			if len(args) >= 3:
				if target not in allusersinroomarray:
					bot.say("I'm sorry, I do not know who you want to transfer money to.")
				else:
					if target == instigator:
						bot.say("You cannot transfer spicebucks to yourself!")
					else:
						success = transfer(bot,  trigger.nick, args[1], args[2])
						if success = 1
						bot.say("You successfully transfered " + str(amount) + " spicebucks to " + target + ".") 
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
    
    
def checkpayday(bot, target, args):
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
		spicebucks(bot, 'SpiceBank', 'plus', taxtotal)
		spicebucks(bot, target, 'minus', taxtotal)
		bot.db.set_nick_value(target, 'spicebucks_taxday', datetoday)
		bot.say("Thank you for reminding me that " + target + " has not paid their taxes today. " + str(taxtotal) + " spicebucks will be transfered to the SpiceBot account.")
	else:
		bot.say("Taxes already paid today.")   

def transfer(bot, instigator, target, amount):
	validamount = 0
	try:
		amount = int(amount)
		validamount = 1
	except:
		bot.say("I'm sorry, the amount you entered does not appear to be a number.")
		validamount = 0

	if validamount == 1:
		if amount <= 0:
			bot.say(instigator + " gave no spicefucks about " + target + "'s comment.")
			validamount = 0
		else:				
			if spicebucks(bot, instigator, 'minus', amount) == 'true':
				spicebucks(bot, target, 'plus', amount)
				validamount = 1
	return validamount
				
						

	

