import sopel.module
import random
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('diabeetus')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    messages = ["Good morning. I'm Wilford Brimley and I'd like to talk to you about Diabeetus.","If you have type 2 Diabeetus, you can get your testing supplies free..."]
    answer = random.randint(0,len(messages) - 1)
    bot.say(messages[answer]);
