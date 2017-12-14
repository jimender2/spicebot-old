import sopel.module
from sopel import module, tools
import sys
import os
import random
import Spicebucks
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('dealme')
def mainfunction(bot, trigger):
  enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
  if not enablestatus:
    execute_main(bot, trigger, triggerargsarray)
        
def execute_main(bot, trigger, arg):
  deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]*4
  bot.say(str(len(deck)))
  myhand,mydeck = deal(deck)
  dealerhand,dealerdeck = deal(deck)
  bot.say('You hand is ' + str(myhand[0]) + ' and ' + str(myhand[1]))  
  bot.say(str(len(mydeck))

def deal(deck):
  hand = []
  for i in range(2):
    random.shuffle(deck)
    card = deck.pop()
    if card == 11:card = "J"
    if card == 12:card = "Q"
    if card == 13:card = "K"
    if card == 14:card = "A"
    hand.append(card)
  return hand, deck
