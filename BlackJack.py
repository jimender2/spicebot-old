import sopel.module
from sopel import module, tools
import sys
import os
import random
import Spicebucks
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *



@sopel.module.commands('roulette', 'spin')
def mainfunction(bot, trigger):
  enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
  if not enablestatus:
    execute_main(bot, trigger, triggerargsarray)
        
def execute_main(bot, trigger, arg):
  bot.say("The dealer isn't here right now')

def payouts(mybet,mynumber,mycolor,winningnumber,color):
  mywinnings=0
  if mynumber == winningnumber:
    mywinnings=mywinnings+(mybet*numberpayout)+mybet
  elif mycolor == color:
    mywinnings=mywinnings+(mybet*colorpayout)+mybet
  return mywinnings
