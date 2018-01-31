"""
Module for getting the bots into an infinite loop
http://sopel.chat
"""

from sopel.module import rule, priority, rate
import random
import time

from SpicebotShared import *

@sopel.module.commands('test')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'test')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    human = random.uniform(0, 30) # Random number with uniform chances across range
    time.sleep(human) # Wait for random time
    prefix = "!"
    command = "test"
    bot.say(prefix + command)
