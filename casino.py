import sopel.module
from sopel import module, tools
import sys
import os
import random
import Spicebucks
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('gamble, casino')
def mainfunction(bot, trigger):
  enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
  if not enablestatus:
    execute_main(bot, trigger, triggerargsarray)
        
def execute_main(bot, trigger, arg):
  #using computer terms instead of fruit
  if arg[0] == 'slots':
    if Spicebucks.spicebucks(bot, trigger.nick, 'minus', 1) == 'true':
      #spicebanktotal = bot.db.get_nick_value('SpiceBank', 'spicebucks_bank') or 0
      #Spicebucks.spicebucks(bot, 'SpiceBank', 'plus', 1 + spicebanktotal)
      #Spicebucks.spicebucks(bot, 'spicebucksslots', 'plus', 1)
      mywinnings = 0
      bot.say(trigger.nick + ' inserts 1 spicebuck and pulls the handle on the slot machine')  
      wheel = ['Modem', 'BSOD'] 
      wheel1 = spin(wheel)
      wheel2 = spin(wheel)
      wheel3 = spin(wheel)
      reel = [wheel1, wheel2, wheel3]
      bot.say('The slot machine displays ' + str(reel))
      for i in reel:
        if i=='BSOD':
           mywinnings = mywinnings + 5
      seen = set()
      seen_add = seen.add
      # adds all elements it doesn't know yet to seen and all other to seen_twice
      seen_twice = set( x for x in reel if x in seen or seen_add(x) )
      bot.say(str(seen_twice))
      # turn the set into a list (as requested)
      if(wheel1 == wheel2 and wheel2 == wheel3):
        bot.say(trigger.nick + ' got 3 ' + str(wheel1))
        if wheel1 == 'BSOD':     
          #spicebanktotal = bot.db.get_nick_value('spicebucksslots', 'spicebucks_bank')
          bot.say('You hit the Jackpot!!! ' + trigger.nick + ' gets ' + str(mywinnings) + '  spicebucks')
          Spicebucks.spicebucks(bot, trigger.nick, 'plus', 1)
        else:
          bot.say('You get 25 spicebucks')
      elif(wheel1 == wheel2 or wheel2==wheel3 or wheel3==wheel1):
        bot.say(trigger.nick + ' got 2 correct and ' + str(mywinnings) + ' spicebucks')
        Spicebucks.spicebucks(bot, trigger.nick, 'plus', 5)
      else:
        bot.say(trigger.nick + ' gets nothing')                   
  

def spin(wheel):
  selected=random.randint(0,(len(wheel)-1))
  reel=wheel[selected]
  return reel
