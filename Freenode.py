import sopel.module
import sys
import os
import random
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

responseperson = ['Dubledore', 'Gandalf', 'Frodo', 'Captain James T. Kirk', 'Rainbow Bright', 'New Kids on the Block']

@sopel.module.commands('msg', 'nick', 'attach', 'server', 'join', 'whois', 'me', 'ban')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    random.shuffle(responseperson)
    if trigger.startswith('.ban') and not trigger.admin:
        bot.say('"You have no power here." - ' + responseperson[0])
    else:
        trigger = trigger.replace('/', trigger, 1)
        bot.say('I believe you wanted to say was ' + trigger)
                
