#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
from sopel import module, tools
import sys
import os
import random
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
import Spicebucks
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

#shared varibles:
maxbet = 100

@sopel.module.commands('gamble', 'casino')
def mainfunction(bot, trigger):
	enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'gamble')
  	if not enablestatus:
    		execute_main(bot, trigger, triggerargsarray)
        
def execute_main(bot, trigger, arg):
	mygame = arg[0]
	if mygame =='slots':
		slots(bot,trigger)
	elif mygame=='blackjack':
		blackjack(bot,trigger,arg)
	elif (mygame=='roulette' or mygame=='spin'):
		roulette(bot,trigger,arg)
	elif mygame=='lottery':
		lottery(bot,trigger,arg)
	elif mygame== 'freebie':
		freebie(bot,trigger)
	elif mygame == 'bank':
		bankbalance=Spicebucks.bank(bot,trigger.nick)
		bot.say(trigger.nick + ' has ' + str(bankbalance) + ' spicebucks in the bank.')	
	elif mygame == 'jackpot':
		bankbalance=Spicebucks.bank(bot,'SpiceBank')
		bot.say('The current jackpot is: ' +str(bankbalance)) 
	elif mygame == 'colors':
		currentcolors =bot.db.get_nick_value('ColorCount','colors') or 0
		bot.say(currentcolors)
		
	elif mygame == 'nocolors':
		bot.db.set_nick_value('ColorCount','colors', 'None')
		bot.say('Colors database emptied')
		
    	else:
        	bot.say('Please choose a game')
		
def freebie(bot,trigger):
	bankbalance=Spicebucks.bank(bot,trigger.nick)
	if bankbalance<1:
		bot.say('The casino gives you 1 Spicebuck for use in the casino')
		Spicebucks.spicebucks(bot, trigger.nick, 'plus', 1)
	else:
		bot.say('Looks like you dont need a handout because your bank balance is ' + str(bankbalance))
		

	
def slots(bot,trigger):
#_____________Game 1 slots___________
#slot machine that uses computer terms with a jackpot tied to how much money has been gambled
	if Spicebucks.transfer(bot, trigger.nick, 'SpiceBank', 1) == 1:
		#add bet to spicebank
		mywinnings = 0
		jackpot = 0
		bot.say(trigger.nick + ' inserts 1 spicebuck and pulls the handle on the slot machine')  
		wheel = ['Modem', 'BSOD', 'RAM', 'CPU', 'RAID', 'VLANS', 'Patches', 'Modem', 'WIFI', 'CPU', 'ClOUD', 'VLANS', 'Patches'] 
		wheel1 = spin(wheel)
		wheel2 = spin(wheel)
		wheel3 = spin(wheel)
		reel = [wheel1, wheel2, wheel3]
		bot.say('The slot machine displays | ' + wheel1 + ' | ' + wheel2 + ' | ' + wheel3 + ' | ')
		for i in reel:
			if i=='BSOD':				
				mywinnings = mywinnings + 1
				bot.say('You got a bonus word, BSOD, worth 1 spicebuck')
		if(wheel1 == wheel2 and wheel2 == wheel3):
			bot.say(trigger.nick + ' got 3 ' + str(wheel1))
			if wheel1 == 'BSOD':
				bankbalance=Spicebucks.bank(bot,'SpiceBank')
				if bankbalance <=500:
					bankbalance=500					
				bot.say(trigger.nick + ' hit the Jackpot of ' + str(bankbalance))
				mywinnings=bankbalance						
			elif wheel1 == 'Patches':
				#bot.say('You got 3 matches')
				mywinnings= mywinnings +5		
			else:
				mywinnings= mywinnings +5
				#bot.say('You got 3 matches')
				
				
		elif(wheel1 == wheel2 or wheel2==wheel3 or wheel3==wheel1):
			mywinnings =  mywinnings + 2
			#bot.say(trigger.nick + ' a match')	
							
		if mywinnings <=0:
			bot.say(trigger.nick + ' gets nothing')
		else:
			bankbalance=Spicebucks.bank(bot,'SpiceBank')
			if mywinnings > bankbalance:
				Spicebucks.spicebucks(bot, trigger.nick, 'plus', mywinnings)
				bot.say(trigger.nick + ' is paid ' + str(mywinnings))
			else:					
				if Spicebucks.transfer(bot, 'SpiceBank', trigger.nick, mywinnings) == 1:
					bot.say(trigger.nick + ' is paid ' + str(mywinnings))
				else:
					bot.say('Error in banking system')
				
					
				
	else:
		bot.say('You dont have enough Spicebucks')

#----------------Roulette-------
def roulette(bot,trigger,arg):
	maxwheel = 25
	minbet=5 #requires at least one payday to play
    	wheel = range(maxwheel + 1)		
    	colors = ['red', 'black']
	inputcheck = 0
	#set bet
    	if len(arg) < 3:
        	bot.say('Please enter an amount to bet')
		inputcheck = 0
	else:
		if not arg[1].isdigit():
			bot.say('Please bet an amount between ' + str(minbet) + ' and ' + str(maxbet))
			inputcheck = 0
		else:
			mybet = int(arg[1])
			inputcheck = 1
    		if (mybet<minbet or mybet>maxbet):
                	bot.say('Please bet an amount between ' + str(minbet) + ' and ' + str(maxbet))			
                	inputcheck = 0
	#setup what was bet on
    	if inputcheck == 1:	
		#check to see if a number was entered
		if arg[2].isdigit(): 
			mynumber = int(arg[2]) 
                    	if(mynumber <= 0 or mynumber > maxwheel):
                        	bot.say('Please pick a number between 0 and ' + str(maxwheel))
                        	inputcheck=0
			#check to see if a color was selected
			else: 
				if len(arg)>=4:
					if (str(arg[3]) == 'red' or str(arg[3]) == 'black'):          
						mycolor = arg[3]
					else:
						bot.say('Choose either red or black')
						inputcheck=0
						mycolor=''
                        	else:
                            		mycolor = ' '
                            		inputcheck =1
		#was a color selected first
		elif(str(arg[2]) == 'red' or str(arg[2]) == 'black'):
	    		mycolor = arg[2]
	    		mynumber=-1
			inputcheck =1
                else:
		#no valid choices
                    bot.say('Please pick either a color or number to bet on')
                    mycolor = ' '
                    mynumber=-1
                    inputcheck = 0 
	# user input now setup game will run
	if inputcheck == 1:
		if Spicebucks.spicebucks(bot, trigger.nick, 'minus', mybet) == 'true':
			Spicebucks.spicebucks(bot, 'SpiceBank', 'plus', mybet)
			bot.say(trigger.nick + ' puts ' + str(mybet) + ' on the table spins and the wheel')
            		winningnumber = spin(wheel)
            		color = spin(colors)
			if bot.nick.endswith('dev'): 					
				currentcolors =bot.db.get_nick_value('ColorCount','colors') or 'None'
				currentcolors = color+str(currentcolors)
				bot.db.set_nick_value('ColorCount','colors', currentcolors)
		 	bot.say('The wheel stops on ' + str(winningnumber) + ' ' + color)
            		mywinnings=0
			if mynumber == winningnumber:
				mywinnings=mybet * maxwheel
			elif mycolor == color: # chance of choosing the same color is so high will set the payout to a fixed amount
				newbet = int(mybet/2)
				colorwinnings = mybet + newbet									
				mywinnings=mywinnings+colorwinnings		
		 	if mywinnings >=1:
				bot.say(trigger.nick + ' has won ' + str(mywinnings))
			 	Spicebucks.spicebucks(bot, trigger.nick, 'plus', mywinnings)		  						
		 	else:
				bot.say(trigger.nick + ' is not a winner')
		else:
			bot.say('You dont have enough Spicebucks')
				
#______Game 3 Lottery________				
def lottery(bot,trigger, arg):
	maxnumber=50
	if(len(arg)<6 or len(arg)>6):
		bot.say('You must enter 5 lottery numbers from 1 to ' + str(maxnumber) + ' to play.')
		success = 0
	else:
		picks = []
		success = 0				
		del arg[0]		
		for pick in arg:
			if pick.isdigit():						
				picks.append(int(pick))
			
		if len(picks)<5:
			bot.say('One of the numbers you entered does not appear to be a number.')
			success = 0
		else:
			success = 1					
		if success == 1:
			pickstemp = picks
			picks = []
			for pick in pickstemp:
				if pick not in picks:
					picks.append(pick)
			if len(picks) < 5:
				bot.say('You must choose 5 different numbers.')
				success = 0					
			if success == 1:
				valid=1
				for pick in picks:
					if(pick > maxnumber or pick < 1):
						valid = 0
				if valid == 0:
					bot.say('One of the numbers you entered is not within the valid range of  1 to ' + str(maxnumber))
				else:
					if Spicebucks.spicebucks(bot, trigger.nick, 'minus', 1) == 'true':
						Spicebucks.spicebucks(bot, 'SpiceBank', 'plus', 1)
						winningnumbers = random.sample(range(1, maxnumber), 5) 
						bot.say('The winning numbers are ' + str(winningnumbers))
						correct = 0
						for pick in picks:
							if pick in winningnumbers:
								correct = correct + 1
						payout = 0
						if correct == 1:
							payout = 1
						elif correct == 2:
							payout = 2
						elif correct == 3:
							payout = 5
						elif correct == 4:
							payout = 20
						elif correct == 5:
							payout = 50
						Spicebucks.spicebucks(bot, trigger.nick, 'plus', payout)
						bot.say("You guessed " + str(correct) + " numbers correctly, and were paid " + str(payout) + " spicebucks.")
					else:
						bot.say('You dont have enough Spicebucks')

							
#____Game 4 Blackjack___
def blackjack(bot,trigger,arg):
	minbet=10
	
	if len(arg)<2:
		bot.say('You must place a bet at least ' + str(minbet) + ' and less then ' + str(maxbet))
	else:
		if not arg[1].isdigit():
			bot.say('Please bet a number between ' + str(minbet) + ' and ' + str(maxbet))
		else:
			mybet=int(arg[1])
			if (mybet<minbet or mybet>maxbet):
				bot.say('Please bet an amount between ' + str(minbet) + ' and ' + str(maxbet))
			else:			
				if Spicebucks.spicebucks(bot, trigger.nick, 'minus', mybet) == 'true':
					deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]*4
					myhand = deal(deck, 2)
					dealerhand = deal(deck, 2)			
					bot.say(trigger.nick + ' has a ' + str(myhand[0]) + ' and a ' + str(myhand[1]) + ' The dealer has a ' + str(dealerhand[1]) + ' showing.')
					myscore = blackjackscore(myhand)
					dealerscore = blackjackscore(dealerhand)
					payout = mybet
					#bot.say('Your score is ' + str(myscore))
					x=0
					dealerhitlist = ''						
					while dealerscore < 18:
						dealerhits=deal(deck, 1)
						dealerhits=dealerhits[0]
						dealerhitlist=dealerhitlist+str(dealerhits)
						dealerhand.append(dealerhits)				
						dealerscore=blackjackscore(dealerhand)
						x=x+1
						if x>4:
							dealerscore=18
					if not dealerhitlist == '':
						hitlist=len(dealerhitlist)
						if hitlist>1:						
							bot.say('The dealer takes ' + str(hitlist)  + ' hits and gets ' + dealerhitlist)
						else: 
							bot.say('The dealer takes a hit and gets a  ' + dealerhitlist) 
						
					if myscore == 21:
						payout=payout + 100
						bot.say(trigger.nick + ' got blackjack and is a winner of ' + str(payout))
						Spicebucks.spicebucks(bot, trigger.nick, 'plus', payout)
					elif myscore > 21:
						bot.say(trigger.nick + ' busted and gets nothing')
					elif myscore < 21:
						dealerwins=''
						if dealerscore > 21:
							payout=payout + 30
							Spicebucks.spicebucks(bot, trigger.nick, 'plus', payout)
							dealerwins = 'the dealer busts '
							bot.say(trigger.nick + ' wins ' + str(payout))
						elif dealerscore < myscore:
							payout=payout + 30
							Spicebucks.spicebucks(bot, trigger.nick, 'plus', payout)
							bot.say(trigger.nick + ' wins ' + str(payout))
						elif dealerscore > myscore:
							dealerwins ='the dealer wins'
						elif dealerscore == myscore:
							payout = payout
							Spicebucks.spicebucks(bot, trigger.nick, 'plus', payout)
							bot.say('It is a draw and no one is a winner or loser')
						if not dealerwins=='':						
							bot.say('The dealer had ' + str(dealerscore) +  ' and ' + dealerwins)
				else:
					bot.say('You do not have enough spicebucks.')
    
  
#__________________________Shared Functions____________________
def spin(wheel):
	random.seed()
	#selects a random element of an array and return one item
  	selected=random.randint(0,(len(wheel)-1))
  	reel=wheel[selected]
  	return reel


def deal(deck, cardcount):
	#choose a random card from a deck and remove it from deck
	hand = []
	
	for i in range(cardcount):
		random.shuffle(deck)
		card = deck.pop()
   		if card == 11:card = "J"
    		if card == 12:card = "Q"
    		if card == 13:card = "K"
	    	if card == 14:card = "A"
	    	hand.append(card)
	return hand	

def blackjackscore(hand):
	myscore = 0
	for card in hand:
		if(card == 'J' or card == 'Q' or card == 'K'):
			myscore = myscore + 10
		elif card=='A':
			testscore = myscore + 10
			if testscore>21:
				myscore = myscore + 1
			else:
				myscore = myscore + 10
		else:
			try:
				myscore = myscore + int(card)
			except ValueError:
				myscore=myscore
	return myscore
