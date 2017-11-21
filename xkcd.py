import sopel.module
import random
import sys
import os
from SpicebotShared import *

maxcomics=1917

@sopel.module.commands('xkcd','comic')
def mainfunction(bot, trigger):
  enablestatus = spicebot_prerun(bot, trigger)
  if not enablestatus:
    execute_main(bot, trigger)
    
def execute_main(bot, trigger):
  if not trigger.group(2):
    mynumber =  getnumber()
  else:
    mynumber = int(trigger.group(2))
    if not 1 >= mynumber <= maxcomics:
      mynumber=getnumber()
  bot.say('https://xkcd.com/' + str(mynumber))
   
def getnumber():
  thenumber = random.randint(0,int(maxcomics))
  if not thenumber or thenumber == '\n':
    thenumber=getnumber()
  return thenumber
