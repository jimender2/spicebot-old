import sopel.module
import random
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('techsupport','itsupport')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    messages = ["YOU MUST CONSTRUCT ADDITIONAL PYLONS!","Have you tried flinging feces at it?","Have you tried chewing the cable?","Did you try turning it off and on again?","Did you try licking the mouse? Double-lick?","Did your try replacing all the ones with zeros?"]
    answer = random.randint(0,len(messages) - 1)
    bot.say(messages[answer]);
