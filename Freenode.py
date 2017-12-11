import sopel.module
import sys
import os
import random
from sopel.module import OP
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

responseperson = ['Dumbledore', 'Gandalf', 'Frodo', 'Captain James T. Kirk', 'Rainbow Bright', 'New Kids on the Block']

@sopel.module.commands('msg', 'nick', 'attach', 'server', 'join', 'whois', 'me', 'ban')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    for c in bot.channels:
        channel = c
    random.shuffle(responseperson)
    operatorarray = []
    for u in bot.channels[channel.lower()].users:
        if bot.privileges[channel.lower()][u] == OP:
            operatorarray.append(u)
    if trigger.startswith('.ban') and trigger.nick.lower() not in operatorarray:
        bot.say('"You have no power here." - ' + responseperson[0])
    else:
        trigger = trigger.replace('.', '/', 1)
        bot.say('I believe you wanted to say was ' + trigger)
                
