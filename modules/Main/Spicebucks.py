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
				if args[1] not in  botusersarray:
					bot.say("I'm sorry, I do not know who " + args[1] + " is.")
				elif args[1] == trigger.nick or args[1] == 'random':
					bankbalance = bank(bot,trigger.nick)
					if bankbalance <=0:
						spicebucks(bot, trigger.nick, 'plus', 15)
						bankbalance = 15
					maxpayout = bankbalance
					randompersons = []
					for u in bot.users:
						if not u==trigger.nick or u==bot.nick:
							randompersons.append(u)
					randomperson = get_trigger_arg(randompersons,'random')			
						
					bot.say(trigger.nick + ' rains Spicebucks down on ' + randomperson)
					winnings=random.randint(1,maxpayout)
					transfer(bot, trigger.nick, randomperson, winnings)
					bot.say(randomperson + " manages to keep " + str(winnings) + " of " + trigger.nick + "'s spicebucks.")
				else:
					target = args[1]
					bankbalance = bank(bot,trigger.nick)
					if bankbalance <=0:
						spicebucks(bot, trigger.nick, 'plus', 15)
						bankbalance = 15
					maxpayout = bankbalance
					bot.action('rains Spicebucks on ' + target)
					winnings=random.randint(1,maxpayout)
					bot.say(target + " manages to keep " + str(winnings) + " of " + trigger.nick + "'s spicebucks")
					transfer(bot, trigger.nick, target, winnings)				
							
			else:
				bot.say(trigger.nick + ' rains Spicebucks on down everyone')
		
		elif args[0] == 'reset' and trigger.admin: #admin only command	
			if len(args) > 1:
				if args[1] == 'spicebank':
					spicebalance = bot.db.get_nick_value('SpiceBank', 'spicebucks_bank') or 0
					spicebucks(bot, 'SpiceBank', 'minus', spicebalance)
					balance = bot.db.get_nick_value('SpiceBank', 'spicebucks_bank') or 0
					bot.say('The spice bank has been robbed and has ' + str(balance) + ' left')
				elif args[1] not in botusersarray:
					bot.say("I'm sorry, I do not know who " + args[1] + " is.")
				else:
					reset(bot,args[1])
					bot.say('Payday reset for ' + args[1])					
			else:
				reset(bot,trigger.nick)
				bot.say('Payday reset for ' + trigger.nick)
		elif args[0] == 'funds' and trigger.admin: #admin only command
			success = 0
			if len(args) > 2: 
				if args[1] == 'spicebank':
					target = 'SpiceBank'
					success = 1
				elif args[1] not in botusersarray:
					bot.say("I'm sorry, I do not know who " + args[1] + " is.")
					success = 0
				else:
					target = args[1]
					success = 1
				if success == 1:
					if args[2].isdigit():
						amount = int(args[2])
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
										
						
                        
                
		elif (args[0] == 'taxes' or args[0] == 'tax'):
			if len(args) > 1:
				if args[1] not in botusersarray:
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
				elif args[1] not in botusersarray:
					bot.say("I'm sorry, I do not know who " + args[1] + " is.")				
				else:
					balance=bank(bot, args[1])                                         
					bot.say(args[1] + ' has '+ str(balance) + " spicebucks in the bank.")
			else:
				balance=bank(bot, trigger.nick)
				bot.say("You have " + str(balance) + " spicebucks in the bank.")       
                     
		elif args[0] == 'transfer':
			if len(args) >= 3:
				target = args[1]
				instigator = trigger.nick
				amount=args[2]
				if not amount.isdigit():
					bot.say('Please enter the person you wish to transfer to followed by an amount you wish to transfer')
				else:	
					amount=int(amount)		
					if target not in  botusersarray:
						bot.say("I'm sorry, I do not know who you want to transfer money to.")
					else:
						if target == instigator:
							bot.say("You cannot transfer spicebucks to yourself!")
						else:
							if amount <=0:								
								bot.say(instigator + " gave no spicefucks about " + target + "'s comment.")
							else:
								balance=bank(bot, trigger.nick)
								if amount <= balance:
									success = transfer(bot,  trigger.nick, target, amount)
									if success == 1:
										bot.say(trigger.nick + " successfully transfered " + str(amount) + " spicebucks to " + target + ".") 
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
				
						

	

