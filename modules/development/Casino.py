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

#Payout lines:
#slots, 77 - roulette, 147 - lottery, 242 - blackjack, 351

#shared variables:
maxbet = 100
wikiurl = 'https://github.com/deathbybandaid/SpiceBot/wiki/Casino'
@sopel.module.commands('gamble', 'casino')
def mainfunction(bot, trigger):
	enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'gamble')
  	if not enablestatus:
    		execute_main(bot, trigger, triggerargsarray)
        
def execute_main(bot, trigger, arg):
	mygame = get_trigger_arg(arg, 1) or 'nocommand'
	if mygame == 'docs' or mygame == 'help':
		bot.say("For help with this module, see here: " + wikiurl)
	elif mygame =='slots':
		slots(bot,trigger,arg)
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
        	bot.say('Please choose a game. Options include: slots, blackjack, roulette, and lottery.')
		
def freebie(bot,trigger):
	bankbalance=Spicebucks.bank(bot,trigger.nick) or 0
	spicebankbalance=Spicebucks.bank(bot, 'SpiceBank') or 0
	if bankbalance<1:
		
		if spicebankbalance >=1:
			bot.say('The casino gives you 1 Spicebuck for use in the casino')
			Spicebucks.transfer(bot, 'SpiceBank', trigger.nick, 1)
		else:
			bot.say("The casino doesn't have any funds to provide")
	else:
		bot.say('Looks like you dont need a handout because your bank balance is ' + str(bankbalance))
		

	
def slots(bot,trigger,arg):
#_____________Game 1 slots___________
#slot machine that uses computer terms with a jackpot tied to how much money has been gambled
#__payouts___
	match3 = 25
	match2 = 5
	bankbalance=Spicebucks.bank(bot,'SpiceBank')
	if bankbalance <=500:
		bankbalance=500
		Spicebucks.spicebucks(bot,'SpiceBank','plus',bankbalance)
				
	keyword = 'BSOD'
	#match3jackpot = jackpot or 500
	mychoice = get_trigger_arg(arg, 2) or 'nocommand'
	if mychoice == 'payout':
		bot.say("Today's jackpot word is " + keyword + " getting it three times will get you " + str(bankbalance) + ". Match 3 and get " + str(match3))
	else:	
#start slots
		if Spicebucks.transfer(bot, trigger.nick, 'SpiceBank', 1) == 1:
			#add bet to spicebank
			mywinnings = 0
			

			wheel = ['Modem', keyword, 'RAM', 'CPU', 'RAID', 'VLANS', 'Patches', 'Modem', 'WIFI', 'CPU', 'ClOUD', 'VLANS', 'Patches'] 
			wheel1 = spin(wheel)
			wheel2 = spin(wheel)
			wheel3 = spin(wheel)
			reel = [wheel1, wheel2, wheel3]
			bot.say(trigger.nick + ' inserts 1 spicebuck and the slot machine displays | ' + wheel1 + ' | ' + wheel2 + ' | ' + wheel3 + ' | ')	
			for i in reel:
				if i==keyword:				
					mywinnings = mywinnings + 1
			if mywinnings>=1:
				bot.say('You got a bonus word, ' + keyword + ', worth 1 spicebuck')

			if(wheel1 == wheel2 and wheel2 == wheel3):
				#bot.say(trigger.nick + ' got 3 ' + str(wheel1))
				if wheel1 == keyword:							
					bot.say(trigger.nick + ' hit the Jackpot of ' + str(bankbalance))
					mywinnings=bankbalance						
				elif wheel1 == 'Patches':
					#bot.say('You got 3 matches')
					mywinnings= mywinnings + match3		
				else:
					mywinnings= mywinnings + match3
					#bot.say('You got 3 matches')


			elif(wheel1 == wheel2 or wheel2==wheel3 or wheel3==wheel1):
				mywinnings =  mywinnings + match2 
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
#------Start Roulutte


#----------------Roulette-------
def roulette(bot,trigger,arg):
	maxwheel = 25
	minbet=15 #requires at least one payday to play
    	wheel = range(maxwheel + 1)		
    	colors = ['red', 'black']
	inputcheck = 0
	
	mybet = get_trigger_arg(arg, 2) or 'nobet'
	myitem = get_trigger_arg(arg, 3) or 'noitem'
	myitem2 = get_trigger_arg(arg, 4) or 'noitem'
	
#__payouts___
	colorpayout = 2 #% of amount bet + amount bet
	#numberpayout = amount bet * numbers of maxwheel
	
	if bot.nick.endswith('dev'): 
		maxwheel=15
	
	#set bet
    	if mybet == 'nobet':
        	bot.say('Please enter an amount to bet')
		inputcheck = 0
	elif mybet=='payout':
		bot.say('Picking the winng number will get you ' + str(maxwheel) + ' X your bet. Picking the winning color will get you your bet plus half the amount bet')
	elif mybet =='end':
		runroulette(bot)

	else:
		if mybet == 'allin':
			balance = Spicebucks.bank(bot, trigger.nick)
			if balance > 0:
				mybet=balance
				inputcheck = 1
			else:
				bot.say('You do not have any spicebucks')
				inputcheck = 0
		elif not mybet.isdigit():
			bot.notice(('Please bet a number between ' + str(minbet) + ' and ' + str(maxbet)),player)
			inputcheck = 0
		else:			
			inputcheck = 1
			mybet = int(mybet)			
			if (mybet<minbet or mybet>maxbet):
				bot.notice(('Please bet an amount between ' + str(minbet) + ' and ' + str(maxbet)), player)			
				inputcheck = 0
	#setup what was bet on
    	if inputcheck == 1:	
		#check to see if a number was entered
		if myitem.isdigit(): 
			mynumber = int(myitem) 
                    	if(mynumber <= 0 or mynumber > maxwheel):
                        	bot.notice(('Please pick a number between 0 and ' + str(maxwheel)),player)
                        	inputcheck=0
			#check to see if a color was selected
			else: 
				if not myitem2 == 'noitem':
					if (str(myitem2) == 'red' or str(myitem2) == 'black'):          
						mycolor = myitem2
					else:
						bot.notice(('Choose either red or black'), player)
						inputcheck=0
						mycolor=''
                        	else:
                            		mycolor = ' '
                            		inputcheck =1
		#was a color selected first
		elif(myitem == 'red' or myitem == 'black'):
	    		mycolor = myitem
	    		mynumber=''
			inputcheck =1
                else:
		#no valid choices
                    bot.notice(('Please pick either a color or number to bet on'),player)                    
                    inputcheck = 0 	
		
		
	# user input now setup game will run
	if inputcheck == 1:
		if Spicebucks.transfer(bot, trigger.nick, 'SpiceBank', mybet) == 1:
			Spicebucks.spicebucks(bot, 'SpiceBank', 'plus', mybet)
			bot.say(trigger.nick + ' puts ' + str(mybet) + ' on the table spins and the wheel')
			bot.db.set_nick_value('Roulette', 'rouletteplayers', player)
			roulettearray = str(mybet) + str(mynumber)+str(mycolor)
			bot.db.set_nick_value(player, 'roulettearray', roulettearray)
		else:
			bot.notice("You don't have enough Spicebucks",player)
			
#-----Run roulette game			
def runroulette(bot):
	players = bot.db.get_nick_value('Roulette', 'rouletteplayers') or ''
	if not players == '':			
		winningnumber = spin(wheel)
		color = spin(colors)		
		spicebankbalance=Spicebucks.bank(bot, 'SpiceBank') or 0
		mywinnings=0
		winners = ''
		totalwon = 0		
		displaymessage = get_trigger_arg(players , "list")
		bot.say('The wheel stops on ' + str(winningnumber) + ' ' + color + ' good luck to ' + displaymessage)
		for player in players:
			playerarray = bot.db.get_nick_value(player, 'roulettearray') or ''
			if not playerarray == '':
				mybet =  int(get_trigger_arg(playerarray,1) or 0)
				mynumber = int(get_trigger_arg(playerarray,2) or 0)
				mycolor =  get_trigger_arg(playerarray,3) or ''
				roulettereset(bot,player)
				if not mybet == 0:
					if mynumber == winningnumber:
						mywinnings=mybet * maxwheel
					elif mycolor == color: # chance of choosing the same color is so high will set the payout to a fixed amount
						newbet = int(mybet/colorpayout)
						colorwinnings = mybet + newbet									
						mywinnings=mywinnings+colorwinnings		
					if mywinnings >=1:
						bot.notice(("You have won " + str(mywinnings),player)
						if spicebankbalance < mywinnings:
							Spicebucks.spicebucks(bot, player, 'plus', mywinnings)		  						
						else:
							Spicebucks.transfer(bot, 'SpiceBank', player, mywinnings)
					   	winners=winners + " " + player
					   	totalwon = totalwon + mywinnings
				   	
						
		if winners =='':
			bot.say("No one wins anything")
		else:
			bot.say(winners + " are winners and " + str(totalwon) + " was won in total")
	else:
	   bot.say("No players found")

		
	
			
def roulettereset(bot,player):
	mybet =''
	mynumber= 0
	mybet = 0
	roulettearray = str(mybet) + str(mynumber)+str(mycolor)
	bot.db.set_nick_value(player, 'roulettearray', roulettearray)					   
					
#______Game 3 Lottery________				
def lottery(bot,trigger, arg):
	maxnumber=50
#___payout table___
	
	#match5payout = jackpot
	if bot.nick.endswith('dev'): 
		maxnumber=20
	bankbalance=Spicebucks.bank(bot,'SpiceBank')
	if bankbalance <=500:
		bankbalance=500	
		Spicebucks.spicebucks(bot,'SpiceBank','plus',bankbalance)
	match1payout = 2
	match2payout = 4
	match3payout = int(0.1 * bankbalance)#% of jackpot
	match4payout = int(0.3 * bankbalance) #% of jackpot
	commandused = get_trigger_arg(arg, 2) or 'nocommand'
	if commandused == 'payout':		
		bot.say("Current lottery jackpot is " + str(bankbalance) + ". Getting 4 number correct pays " + str(match4payout) + " and getting 3 correct = " + str(match3payout))
		success = 0	
	else:
		picks = []
		success = 0	
		
		picklen=len(arg)+1		
		for i in range(0,picklen):
			picker = get_trigger_arg(arg, i)
			if picker.isdigit():
				picks.append(int(picker))
		
		
		if len(picks)!=5:
			bot.say('You must enter 5 lottery numbers from 1 to ' + str(maxnumber) + ' to play.')
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
					if Spicebucks.transfer(bot, trigger.nick, 'SpiceBank', 1) == 1:
						
						winningnumbers = random.sample(range(1, maxnumber), 5) 
						bot.say('The winning numbers are ' + str(winningnumbers))
						correct = 0
						for pick in picks:
							if pick in winningnumbers:
								correct = correct + 1
						payout = 0
										
						if correct == 1:
							payout = match1payout
						elif correct == 2:
							payout = match2payout
						elif correct == 3:
							payout =  match3payout
						elif correct == 4:
							payout = match4payout
						elif correct == 5:							
							payout = bankbalance
												
						
						if payout > 0:							
							bot.say("You guessed " + str(correct) + " numbers correctly, and were paid " + str(payout) + " spicebucks.")
							Spicebucks.transfer(bot, 'SpiceBank', trigger.nick, payout)
						else:
							bot.say('You are not a winner')
						
					else:
						bot.say('You dont have enough Spicebucks')

							
#____Game 4 Blackjack___
def blackjack(bot,trigger,arg):
	minbet=30
	blackjackpayout = 2
	beatdealerpayout = 2
	payouton21 = 1
	mychoice =  get_trigger_arg(arg, 2) or 'nocommand'
	mychoice2 = get_trigger_arg(arg, 3) or 'nocommand'
	botusersarray = get_botdatabase_value(bot, bot.nick, 'botusers') or []
	botuseron=[]
	for u in bot.users:
		if u in botusersarray and u != bot.nick:
			botuseron.append(u)
	if mychoice == 'nocommand':
		bot.say("Use .gamble blackjack deal <bet> amount to start a new game")
		
	else:
		deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]*4
		myhand = []
		dealerhand = []
		player=trigger.nick
		payout = 0
		if(mychoice == 'deal' or mychoice == 'start' or mychoice == '1'):
			if mychoice2 == 'nocommand':
				bot.say("Please enter an amount you wish to bet")
			else:
				if not mychoice2.isdigit():
					bot.say('Please bet a number between ' + str(minbet) + ' and ' + str(maxbet))
				else:							
					mybet=int(mychoice2)
					if (mybet<minbet or mybet>maxbet):
						bot.say('Please bet an amount between ' + str(minbet) + ' and ' + str(maxbet))
					else:			
						if Spicebucks.transfer(bot, player, 'SpiceBank', mybet) == 1:
							#reset write blank hand
							blackjackreset(bot,player)
							myhand = deal(deck, 2)
							dealerhand = deal(deck, 2)			
							bot.say(player + ' has a ' + str(myhand[0]) + ' and a ' + str(myhand[1]) + ' The dealer has a ' + str(dealerhand[1]) + ' showing.')
							myscore = blackjackscore(myhand)
							dealerscore = blackjackscore(dealerhand)
							payout = mybet
							if myscore == 21:
								payout=payout + (mybet*blackjackpayout) 
								bot.say(player + ' got blackjack and wins ' + str(payout))
								Spicebucks.spicebucks(bot, player, 'plus', payout)
							else:							
								
								#update hand in the database
								bot.db.set_nick_value(player, 'myhand', myhand)
								bot.db.set_nick_value(player, 'dealerhand', dealerhand)
								bot.db.set_nick_value(player, 'mybet', mybet)
								bot.say( " You can say'.gamble blackjack 2' to take a card or '.gamble blackjack 3' to finish the game")

						
						else:
							bot.say('You do not have enough spicebucks.')
		elif mychoice == 'hit' or mychoice == '2':
			myhand =  bot.db.get_nick_value(player, 'myhand') or 0
			#dealerhand = bot.db.get_nick_value(player, 'dealerhand') or 0
			if (myhand == [] or myhand ==0):
				bot.say('Use deal to start a new game')
			else:
				playerhitlist = ''
				#bot.say(player + ' has ' + str(myhand))
				#bot.say('The dealer has ' + str(dealerhand))
				playerhits=deal(deck, 1)
				playerhits=playerhits[0]				
				
				myhand.append(playerhits)
				myscore = blackjackscore(myhand)
				if myscore >21 and len(myhand) > 2:
					if myhand[0] == 'A': 			
						myhand[0]=1
					if myhand[1] == 'A':
						myhand[1] = 1
					myscore= blackjackscore(myhand)			
				if myscore < 21:				
					bot.db.set_nick_value(player, 'myhand', myhand)
					bot.say(player + " takes a hit and a gets a " +  str(playerhits) + " " + player + "'s score is now " + str(myscore))
				else:
					bot.say(player + ' got ' + str(playerhits) + ' busted and gets nothing')
					blackjackreset(bot,player)
					
		elif mychoice == 'check':
			target = get_trigger_arg(arg, 3) or 'notarget'						
			if not target.lower() in [u.lower() for u in botuseron]:
				bot.say("Target not found.")
			else:					
				myhand =  bot.db.get_nick_value(target, 'myhand') or 0
				dealerhand = bot.db.get_nick_value(target, 'dealerhand') or 0
				bot.say(target + ' has ' + str(myhand) + ' The dealer has ' + str(dealerhand))

		elif mychoice == 'double' or mychoice == '4':
			myhand =  bot.db.get_nick_value(player, 'myhand') or 0
			payout = bot.db.get_nick_value(player, 'mybet') or 0
			if (myhand == [] or myhand ==0):
				bot.say('Use deal to start a new game')
			else:
				if len(myhand) == 2:
					mybet=payout+payout
					bot.db.set_nick_value(player, 'mybet', mybet)
					playerhitlist = ''
					#bot.say(player + ' has ' + str(myhand))
					#bot.say('The dealer has ' + str(dealerhand))
					playerhits=deal(deck, 1)
					playerhits=playerhits[0]		
					myhand.append(playerhits)
					bot.db.set_nick_value(player, 'myhand', myhand)
					bot.say(player + " doubles down and gets " + str(playerhits))
					blackjackstand(bot,player,myhand,dealerhand,mybet)					
		
						
		elif mychoice == 'adminset' and trigger.admin:
			target = get_trigger_arg(arg, 3) or 'notarget'
			card1 = get_trigger_arg(arg, 4) or 'nocard1'
			card2 = get_trigger_arg(arg, 5) or 'nocard2'
			myhand = []
			dealerhand = []
			mybet = 30
			if not target.lower() in [u.lower() for u in botuseron]:
				bot.say("Target not found.")
			else:
				if not (card1 == 'nocard1'and card2 == 'nocard2'):
					myhand.append(card1)
					myhand.append(card2)
					dealerhand.append(card1)
					dealerhand.append(card2)
					bot.say(str(myhand))					
					bot.db.set_nick_value(player, 'myhand', myhand)
					bot.db.set_nick_value(player, 'dealerhand', dealerhand)
					bot.db.set_nick_value(player, 'mybet', mybet)				
									
			
			
		elif mychoice == 'stand' or mychoice == '3':
			myhand =  bot.db.get_nick_value(player, 'myhand') or 0
			dealerhand = bot.db.get_nick_value(player, 'dealerhand') or 0
			payout = bot.db.get_nick_value(player, 'mybet') or 0
			blackjackstand(bot,player,myhand,dealerhand,payout)
			
			
		elif mychoice == 'payout':
			bot.say("Getting blackjack pays 2x, getting 21 pays 1x, beating the dealer pays 1/2 your bet.")
				

		else:
			bot.say('Choose an option: deal, hit, or stand')

			
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
		card = get_trigger_arg(deck,'random')	
   		if card == 11:card = "J"
    		if card == 12:card = "Q"
    		if card == 13:card = "K"
	    	if card == 14:card = "A"
	    	hand.append(card)
	return hand	

def blackjackstand(bot,player,myhand,dealerhand,payout):
	deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]*4
	if (myhand == [] or myhand ==0):
		bot.say('Use deal to start a new game')
	else:
		myscore = blackjackscore(myhand)
		if myscore >21 and len(myhand) > 2:
			if myhand[0] == 'A': 			
				myhand[0]=1
			if myhand[1] == 'A':
				myhand[1] = 1
			myscore= blackjackscore(myhand)				

		dealerscore = blackjackscore(dealerhand)				
		dealerwins=''
		if myscore == 21:
			payout=payout + payout
			bot.say(player + ' got blackjack and is a winner of ' + str(payout))
			Spicebucks.spicebucks(bot, player, 'plus', payout)
		elif myscore > 21:
			bot.say(player + ' busted and gets nothing')
		elif myscore < 21:

			dealerhitlist = ''						
			while dealerscore < 18:
				dealerhits=deal(deck, 1)
				dealerhits=dealerhits[0]
				dealerhitlist=dealerhitlist + ' ' + str(dealerhits)
				dealerhand.append(dealerhits)				
				dealerscore=blackjackscore(dealerhand)

			if not dealerhitlist == '':
				hitlist=len(dealerhitlist)-2 #minus two for spaces
				if hitlist>1:						
					bot.say('The dealer takes ' + str((hitlist))  + ' hits and gets' + dealerhitlist)
				else: 
					bot.say('The dealer takes a hit and gets a' + dealerhitlist)
			showdealerhand = ''
			for i in dealerhand:						
				showdealerhand = showdealerhand + " " + str(i)
		
			if dealerscore > 21:
				payout=payout + int((payout/2))
				Spicebucks.spicebucks(bot, player, 'plus', payout)
				bot.say("The dealer had " + showdealerhand + " busts")
				bot.say(player + ' wins ' + str(payout))
			elif dealerscore == 21:
				bot.say("The dealer has " + showdealerhand + " and wins")
			elif dealerscore < myscore:
				payout=payout + int((payout/2))
				Spicebucks.spicebucks(bot, player, 'plus', payout)
				bot.say("The dealer had " + showdealerhand + " " + player + " wins " + str(payout))
			elif dealerscore > myscore:
				bot.say("The dealer had " +  showdealerhand + " and wins")
			elif dealerscore == myscore:			
				Spicebucks.spicebucks(bot, player, 'plus', payout)
				bot.say('It is a draw and ' + player + ' gets ' + str(payout))
			else:
				bot.say('No scores found start a new game')


		blackjackreset(bot,player)

def blackjackscore(hand):
	myscore = 0
	for card in hand:
		if(card == 'J' or card == 'Q' or card == 'K'):
			myscore = myscore + 10
		elif card=='A':
			testscore = myscore + 11
			if testscore>21:
				myscore = myscore + 1
			else:
				myscore = myscore + 11
		else:
			try:
				myscore = myscore + int(card)
			except ValueError:
				myscore=myscore
	return myscore

def blackjackreset(bot,player):
	myhand = []
	dealerhand = []
	mybet = 0
	bot.db.set_nick_value(player, 'myhand', myhand)
	bot.db.set_nick_value(player, 'dealerhand', dealerhand)
	bot.db.set_nick_value(player, 'mybet', mybet)
