import sopel.module
from sopel import module, tools
import sys
import os
import random
import Spicebucks
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *


#A roulette game to be used with Spicebucks.
maxwheel = 24
numberpayout = 2
colorpayout = 1
evenpayout = 3

@sopel.module.commands('roulette', 'spin')
def mainfunction(bot, trigger):
	enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
	if not enablestatus:
		execute_main(bot, trigger, triggerargsarray)
        
def execute_main(bot, trigger, arg):
	inputcheck=0
	
	if not (len(arg)>3 or len(arg)<1):
		if str(arg[0])=='payout':
			bot.say('Picking the correct number gives 4 times your bet. Picking the correct color gives double your bet')
			inputcheck=0
		#elif str(arg[0])=='betitall':			
			#spicebucks = bot.db.get_nick_value(trigger.nick, 'spicebucks_bank') or 0
			#bot.say(trigger.nick + ' is going all in and letting ' + str(spicebucks) + ' ride.')
			#mybet=spicebucks
			#inputcheck=1
		elif not arg[0].isdigit():
			bot.say('Please enter your bet followed by number and/or the color you wish to bet on')
			inputcheck=0
		else:
			mywinnings=0
			if len(arg) == 3:
				if not int(arg[0])>=1:      
					bot.say('Please enter the amount you wish to bet first')
					inputcheck=0
				elif not (int(arg[1])<=maxwheel and int(arg[1])>=1):
					bot.say('Please pick a number between 1 and ' + str(maxwheel))
					inputcheck=0
				elif not (arg[2] == 'red' or arg[2] == 'black'):
					bot.say('Please select either red or black')	
					inputcheck=0
				else:        
					mybet=int(arg[0])
					mynumber=int(arg[1])
					mycolor=arg[2]					
	    				inputcheck = 1	
			elif len(arg)==2:  			
				mybet = int(arg[0])
				if(str(arg[1]) == 'red' or str(arg[1]) == 'black'):
					mycolor = arg[1]
					mynumber=-1
					inputcheck =1
				elif arg[1].isdigit():
					if(int(arg[1])<=maxwheel and int(arg[1])>=1):
						mynumber=int(arg[1])
						mycolor=' '
						inputcheck = 1
					else:
						bot.say('Please pick a number between 1 and ' + str(maxwheel))
						inputcheck=0
				else:
					bot.say('You have choosen to bet on black')
					mycolor='black'
					mynumber=0
					inputcheck = 1
					        
		if inputcheck==1:
			if mybet<=0:
				bot.say('Please enter your bet followed by number and the color you wish to bet on')
			else:
				if Spicebucks.spicebucks(bot, trigger.nick, 'minus', mybet) == 'true':
					bot.say(trigger.nick + ' puts ' + str(mybet) + ' on the table spins and the wheel')
					winningnumber,color = spinwheel()  	    						
					bot.say('The wheel stops on ' + str(winningnumber) + ' ' + color)
					mywinnings=payouts(mybet,mynumber,mycolor,winningnumber,color)
					if mywinnings >=1:
						bot.say(trigger.nick + ' has won ' + str(mywinnings))
						Spicebucks.spicebucks(bot, trigger.nick, 'plus', mywinnings)		  						
					else:
						bot.say(trigger.nick + ' is a loser')      
	else:
		bot.say('Please enter your bet followed by number and or the color you wish to bet on') 	
        
         
def spinwheel():
  	random.seed()
	thenumber = random.randint(1,maxwheel)
	thecolor=random.randint(0,1)
	#return array with color and number
	if thecolor == 0:
		color = 'black'
		#blacktotal = bot.db.get_nick_value('roulette', 'roulette_blacks') or 0
		#bot.db.set_nick_value('roulette', 'roulette_blacks', blacktotal + 1)
	else:
		color = 'red' 
		#redtotal = bot.db.get_nick_value('roulette', 'roulette_reds') or 0
		#bot.db.set_nick_value('roulette', 'roulette_reds', redtotal + 1)
	return thenumber, color

def payouts(mybet,mynumber,mycolor,winningnumber,color):
	mywinnings=0
	if mynumber == winningnumber:
		mywinnings=mywinnings+(mybet*numberpayout)+mybet
	elif mycolor == color:
		mywinnings=mywinnings+(mybet*colorpayout)+mybet
	return mywinnings
