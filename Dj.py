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
        bot.say(trigger.nick + ' puts a nickel in the jukebox and it start to playing ' + song)
    else:
        bot.say('The jukebox starts playing ' + 'Never Gonna Give You Up')

def getsong():
    htmlfile=urllib.urlopen(fra)
    lines=htmlfile.read().splitlines()
    mysong=random.choice(lines)
    if not mysong or mysong == '\n':
       mysong = randomfra()
    return mysong
