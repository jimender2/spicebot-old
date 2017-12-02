import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('matrix')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    if trigger.group(2):
        if trigger.group(2) == 'redpill':
            bot.say('You take the red pill, you stay in Wonderland, and I show you how deep the rabbit hole goes.')
        elif trigger.group(2) == 'bluepill':
            bot.say('You take the blue pill, the story ends. You wake up in your bed and believe whatever you want to believe.')
        else:
            normalrun='true'
    else:
        normalrun='true'
    try:
        if normalrun:
            bot.say('You have two choices. redpill Or bluepill')        
    except UnboundLocalError:
        return
