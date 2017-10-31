import sopel.module
from Spicebot_Shared import *

@sopel.module.rate(120)
@sopel.module.commands('airbiscuit','float','floats')
def mainfunction(bot, trigger):
    check_disenable(bot, target)
    
def execute_main(bot, trigger):
    if target == trigger.nick:
        bot.say(trigger.nick + " floats an air biscuit.")
