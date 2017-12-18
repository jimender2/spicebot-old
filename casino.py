import sopel.module
from sopel import module, tools
import sys
import os
import random
import Spicebucks
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('gamble', 'casino')
def mainfunction(bot, trigger):
	enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
  	if not enablestatus:
    		execute_main(bot, trigger, triggerargsarray)
        
def execute_main(bot, trigger, arg):
	#shared varibles:
	maxbet = 100
	if len(arg)>=1:
	#_____________Game 1 slots___________
		if arg[0] == 'slots':
		#slot machine that uses computer terms with a jackpot tied to how much money has been gambled
			if Spicebucks.spicebucks(bot, trigger.nick, 'minus', 1) == 'true':
				mywinnings = 0
				bot.say(trigger.nick + ' inserts 1 spicebuck and pulls the handle on the slot machine')  
				wheel = ['Modem', 'BSOD', 'RAM', 'CPU', 'RAID5'] 
				wheel1 = spin(wheel)
				wheel2 = spin(wheel)
				wheel3 = spin(wheel)
				reel = [wheel1, wheel2, wheel3]
				bot.say('The slot machine displays ' + str(reel))
				for i in reel:
					if i=='BSOD':
				 		mywinnings = mywinnings + 5
				
				if(wheel1 == wheel2 and wheel2 == wheel3):
					bot.say(trigger.nick + ' got 3 ' + str(wheel1))
					if wheel1 == 'BSOD':
						mywinnings = 1000
						bot.say('You hit the Jackpot!!! ' + trigger.nick + ' gets ' + str(mywinnings) + '  spicebucks')
						Spicebucks.spicebucks(bot, trigger.nick, 'plus', mywinnings)
					else:
						bot.say('You get 25 spicebucks')
				elif(wheel1 == wheel2 or wheel2==wheel3 or wheel3==wheel1):
					mywinnings = 5
					bot.say(trigger.nick + ' got 2 correct and ' + str(mywinnings) + ' spicebucks')
					Spicebucks.spicebucks(bot, trigger.nick, 'plus', mywinnings)
				else:
					bot.say(trigger.nick + ' gets nothing')

		#__________Game 2 Roulette________________
		elif arg[0] == 'roulette':
			maxwheel = 25
			wheel = range(maxwheel + 1)		
			colors = ['red', 'black']
			if len(arg) < 3:
				bot.say('Please enter an amount to bet')
				inputcheck = 0
			else:
				if not arg[1].isdigit():
					bot.say('Please bet an amount between 1 and ' + str(maxbet))
					inputcheck = 0
				else:
					mybet = int(arg[1])
					inputcheck = 1
				if (mybet<=0 or mybet>maxbet):
					bot.say('Please bet an amount between 1 and ' + str(maxbet))				
					inputcheck = 0
				if inputcheck == 1:		
					if arg[2].isdigit():
						mynumber = int(arg[2])
						if(mynumber <= 0 or mynumber > maxwheel):
							bot.say('Please pick a number between 0 and ' + str(maxwheel))
							inputcheck=0
						else:
							if len(arg)>=4:
								if (str(arg[3]) == 'red' or str(arg[3]) == 'black'):          
									mycolor = arg[3]
								else:
									mycolor='' 
							else:
								mycolor = ' '
							inputcheck =1
					elif(str(arg[2]) == 'red' or str(arg[2]) == 'black'):
						mycolor = arg[2]
						mynumber=-1
						inputcheck =1
					else:
						bot.say('Please pick either a color or number to bet on')
						mycolor = ' '
						mynumber=-1
						inputcheck = 0
					if inputcheck == 1:
						if Spicebucks.spicebucks(bot, trigger.nick, 'minus', mybet) == 'true':
							bot.say(trigger.nick + ' puts ' + str(mybet) + ' on the table spins and the wheel')
							winningnumber = spin(wheel)
							color = spin(colors)
							bot.say('The wheel stops on ' + str(winningnumber) + ' ' + color)
							mywinnings=payouts(mybet,mynumber,mycolor,winningnumber,color)
							if mywinnings >=1:
								bot.say(trigger.nick + ' has won ' + str(mywinnings))
								Spicebucks.spicebucks(bot, trigger.nick, 'plus', mywinnings)		  						
							else:
								bot.say(trigger.nick + ' is a loser')
	else:
		bot.say('Please select a game')
						

           
    
  
#__________________________Shared Functions____________________
def spin(wheel):
	#selects a random element of an array and return one item
  	selected=random.randint(0,(len(wheel)-1))
  	reel=wheel[selected]
  	return reel

def payouts(mybet,mynumber,mycolor,winningnumber,color):
	mywinnings=0
	if mynumber == winningnumber:
		mywinnings=mywinnings+(mybet*2)+mybet
	elif mycolor == color:
		mywinnings=mywinnings+(mybet*1)+mybet
	return mywinnings
