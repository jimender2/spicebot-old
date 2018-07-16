import sopel.module
import random
import urllib
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

devcookies='https://raw.githubusercontent.com/deathbybandaid/SpiceBot/dev/Text-Files/fortune_cookie.txt'
cookies='https://raw.githubusercontent.com/deathbybandaid/SpiceBot/master/Text-Files/fortune_cookie.txt'
devbot='dev' ## Enables the bot to distinguish if in test

@sopel.module.commands('fortune','cookie')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'fortune')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)

def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    if not bot.nick.endswith(devbot):
        filetocheck=cookies #Master branch
    else:
        filetocheck=devcookies #Dev branch
    myline = randomcookie(filetocheck)
    bot.say(myline)

# random cookie
def randomcookie(filetocheck):
    htmlfile=urllib.urlopen(filetocheck)
    lines=htmlfile.read().splitlines()
    myline=random.choice(lines)
    if not myline or myline == '\n':
        myline = randomcookie(filetocheck)
    return myline
