import sopel.module
import random
import urllib
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

fra='https://raw.githubusercontent.com/deathbybandaid/SpiceBot/master/Text-Files/momsspaghetti.txt'

@sopel.module.commands('eminem')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)

def execute_main(bot, trigger, triggerargsarray):
    if not trigger.group(2):
        myline = randomfra()
        bot.say(myline)

# random rule
def randomfra():
    htmlfile=urllib.urlopen(fra)
    lines=htmlfile.read().splitlines()
    myline=random.choice(lines)
    if not myline or myline == '\n':
        myline = randomfra()
    return myline
