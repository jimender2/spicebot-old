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
maxwheel = 19

@sopel.module.commands('roulette', 'spin')
def mainfunction(bot, trigger):
  enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
  if not enablestatus:
    execute_main(bot, trigger, triggerargsarray)
        
def execute_main(bot, trigger, arg):
  #get triggerwords from player to allow number,color and even/odd choices
  if len(arg) < 3:
    bot.say("Please enter your bet followed by number or color you wish to bet on")	
  else:
    if not int(arg[0])>=1:      
      bot.say('Please enter the amount you wish to bet first')
    elif not int(arg[1])<=maxwheel and int(arg[1])>=1:
      bot.say('Please pick a number between 1 and ' + str(maxwheel))
    elif not arg[2] == 'red' or arg[2] == 'black':
      bot.say("Please select either red or black")	
    else:
      mybet=int(arg[0])
      mynumber=int(arg[1])
      mycolor=arg[2]                         
      bot.say(trigger.nick + ' puts ' + str(mybet) + 'on the table spins the wheel')
      winningnumber,pickedcolor = spinwheel()  
      if pickedcolor == 0:
        color = 'black'
      else:
        color = 'red' 
      bot.say('The wheel stops on ' + str(winningnumber) + ' ' + color)
      if winningnumber==mynumber or color==color:
        bot.say(trigger.nick + ' is a winner')    
      
def spinwheel():
  random.seed()
  thenumber = random.randint(0,maxwheel)
  thecolor=random.randint(0,1)
  #return array with color and number
  return thenumber, thecolor
