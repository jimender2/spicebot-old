import sopel.module
import urllib
import sys
import os
sys.path.append(moduledir)
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
  if not mynumber>=1 & <=maxcomics
    mynumber=getnumber()
  bot.say('https://xkcd.com/' + mynumber)
   
def getnumber():
  thenumber = random.range(0,maxcomics,2)
  if not thenumber or thenumber == '\n':
    thenumber=getnumber()
  return thenumber
