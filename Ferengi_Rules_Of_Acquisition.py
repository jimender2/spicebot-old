import sopel.module
import random
import urllib
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

fra='https://raw.githubusercontent.com/deathbybandaid/sopel-modules/dev/otherfiles/ferengi_rules.txt'

@sopel.module.rate(120)
@sopel.module.commands('ferengi')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    if not trigger.group(2):
        myline = randomfra()
    else:
        rulenumber = int(trigger.group(2))
        htmlfile=urllib.urlopen(fra)
        lines=htmlfile.readlines()
        try:
            myline = str(lines[rulenumber-1])
        except IndexError:
            myline = 'That doesnt appear to be a rule number.'
        if not myline or myline == '\n':
            myline = 'There is no cannonized rule tied to this number.'
    bot.say(myline)
       
# random rule
def randomfra():
    htmlfile=urllib.urlopen(fra)
    lines=htmlfile.read().splitlines()
    myline=random.choice(lines)
    if not myline or myline == '\n':
        myline = randomfra()
    return myline
