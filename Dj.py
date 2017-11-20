import sopel.module
import random
import urllib
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

fra='https://raw.githubusercontent.com/deathbybandaid/sopel-modules/master/otherfiles/jukebox_party.txt'


@sopel.module.commands('dj')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    song = getsong()
       if song:
		  bot.say(trigger.nick + 'put in a nickel and plays ' + song)
       else:
          bot.say(trigger.nick + 'put in a nickel and plays ' + 'Never Gonna Give You Up by Rick Astley')

def getsong():
    htmlfile=urllib.urlopen(fra)
    lines=htmlfile.read().splitlines()
    mysong=random.choice(lines)
    if not mysong or myline == '\n':
       mysong = randomfra()
    return mysongsong
