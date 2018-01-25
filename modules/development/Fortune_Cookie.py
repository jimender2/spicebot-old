import sopel.module
import random
import urllib
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

cookies='https://raw.githubusercontent.com/deathbybandaid/SpiceBot/dev/Text-Files/fortune_cookie.txt'

@sopel.module.commands('fortune','cookie')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, 'fortune')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
    if not trigger.group(2):
        myline = randomcookie()
        bot.say(myline)
       
# random rule
def randomcookie():
    htmlfile=urllib.urlopen(cookies)
    lines=htmlfile.read().splitlines()
    myline=random.choice(lines)
    if not myline or myline == '\n':
        myline = randomcookie()
    return myline
