import sopel.module
from random import random
from random import randint
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('wanted')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    rando = randint(2, 50)
    if not trigger.group(2):
        bot.say('You must choose a Person.')
    elif not trigger.group(2).strip() == bot.nick:
        bot.say(trigger.group(2).strip() + ' was never wanted as a child, but now is wanted in ' + str(rando) + ' states!')
