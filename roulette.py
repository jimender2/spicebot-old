import sopel.module
from sopel import module, tools
import sys
import os
import random
#import Spicebucks.py
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *


#A roulette game to be used with Spicebucks.


@sopel.module.commands('roulette', 'spin')
def mainfunction(bot, trigger):
  enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
  if not enablestatus:
    execute_main(bot, trigger, triggerargsarray)
        
def execute_main(bot, trigger, triggerargsarray):
  #get triggerwords from player to allow number,color and even/odd choices
  bot.say(trigger.nick + ' spins the wheel')
  results = spinwheel()
  winningnumber = results[0]
  if results[1] == 0:
    color = 'black'
  else:
    color = 'red' 
  bot.say('The wheel stops on ' + str(winningnumber) + ' ' + color) 
  #payout based on results

def spinwheel():
  random.seed()
  thenumber = random.randint(0,36)
  thecolor=random.randint(0,1)
  #return array with color and number
  return result[thenumber, thecolor]
