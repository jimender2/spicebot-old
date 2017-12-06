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
  if arg(0)=='payout':
    bot.say('Picking the correct number gives 4 times your bet. Picking the correct number gives double your bet')
  else:
    if len(arg) < 3:
      bot.say("Please enter your bet followed by number or color you wish to bet on")	
    else:
      if not int(arg[0])>=1:      
        bot.say('Please enter the amount you wish to bet first')
      elif not (int(arg[1])<=maxwheel and int(arg[1])>=1):
        bot.say('Please pick a number between 1 and ' + str(maxwheel))
      elif not (arg[2] == 'red' or arg[2] == 'black'):
        bot.say("Please select either red or black")	
      else:
        if Spicebucks.spicebucks(bot, trigger.nick, 'minus', mybet) == 'true':
          mywinnings=0
          mybet=int(arg[0])
          mynumber=int(arg[1])
          mycolor=arg[2]         
          bot.say(trigger.nick + ' puts ' + str(mybet) + ' on the table spins the wheel')
          winningnumber,pickedcolor = spinwheel()  
          if pickedcolor == 0:
            color = 'black'
          else:
            color = 'red' 
          bot.say('The wheel stops on ' + str(winningnumber) + ' ' + color)
          if mynumber == winningnumber:
            mywinnings=mywinnings+(mybet*4)
          elif mycolor == color:
            mywinnings=mywinnings+mybet
          if mywinnings >=1:
            bot.say(trigger.nick + ' has won ' + mywinnings)
            Spicebucks.spicebucks(bot, trigger.nick, 'plus', mywinnings)
            Spicebucks.spicebucks(bot, trigger.nick, 'plus', mybet)
          else:
            bot.say(trigger.nick + ' has lost ' + mybet)
        else:
          bot.say('You do not have enough Spicebucks for your bet')
      
def spinwheel():
  random.seed()
  thenumber = random.randint(0,maxwheel)
  thecolor=random.randint(0,1)
  #return array with color and number
  return thenumber, thecolor
