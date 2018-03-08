#http://dilbert.com/search_results?terms=cats
import sopel.module
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('dilbert')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'dilbert')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)

def execute_main(bot, trigger,triggerargsarray):    
    #No input
    target = get_trigger_arg(bot,triggerargsarray,0)                                                     
    if not target:
        return bot.say('http://dilbert.com')
    bot.say('http://dilbert.com/search_results?terms=' + target.replace(' ', '+'))
