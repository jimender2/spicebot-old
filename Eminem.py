import sopel.module
import random
import urllib
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

fra='https://raw.githubusercontent.com/deathbybandaid/sopel-modules/master/otherfiles/momsspaghetti.txt'

@sopel.module.commands('eminem')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
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
