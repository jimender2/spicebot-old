import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.rate(120)
@sopel.module.commands('airbiscuit','float','floats')
def mainfunction(bot, trigger):
    check_disenable(bot, trigger)
    
def execute_main(bot, trigger):
    if target == trigger.nick:
        bot.say(trigger.nick + " floats an air biscuit.")
