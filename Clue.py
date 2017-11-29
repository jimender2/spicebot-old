import sopel.module
import sys
import os
import random
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('clue')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)

rooms = ['Ballroom', 'Billiard Room', 'Cellar', 'Conservatory', 'Dining Room', 'Kitchen', 'Hall', 'Library', 'Lounge', 'Study', 'secret passage']
weapons = ['Candlestick', 'Knife', 'Lead Pipe', 'Revolver', 'Rope', 'Candlestick', 'Knife', 'Lead Pipe', 'Revolver', 'Rope', 'Wrench', 'Wrench']
    
def execute_main(bot, trigger):
    players = []
    for c in bot.channels:
        channel = c
    for u in bot.channels[channel].users:
        target = u
        if get_spicebotdisenable(bot, target):
            players.append(target)
    random.shuffle(rooms)
    random.shuffle(weapons)
    random.shuffle(players)
    if rooms[0] == 'secret passage':
        bot.say(players[1] + " evaded " + players[0] + " by using the secret passage. So " + players[0] + " killed " + players[2] + " with the " + weapons[0] + " instead.")    
    else:
        bot.say(players[0] + " killed " + players[1] + " in the " + rooms[0] + " with the " + weapons[0] + ".")
        
    if trigger.group(2) == players[0]:
            bot.say('You guessed the killer correctly!')
    if trigger.nick == players[0]:
            bot.say('YOU ARE THE KILLER!')
