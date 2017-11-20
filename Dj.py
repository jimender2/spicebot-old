import sopel.module
import random
import urllib
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

party='https://raw.githubusercontent.com/deathbybandaid/sopel-modules/master/otherfiles/jukebox_party.txt'
friday='https://raw.githubusercontent.com/deathbybandaid/sopel-modules/master/otherfiles/jukebox_friday.txt'



@sopel.module.commands('dj')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    if not trigger.group(2):
       playlist=party
    else:
	query = trigger.group(2).replace(' ','20%')
	query = str(query)
	playlist = getplaylist(query)
		
    song = getsong(playlist)
    if song:
       bot.say(trigger.nick + ' puts a nickel in the jukebox and it start to playing ' + song)
    else:
	bot.say('The jukebox starts playing ' + 'Never Gonna Give You Up')

def getsong(playlist):
    htmlfile=urllib.urlopen(playlist)
    lines=htmlfile.read().splitlines()
    mysong=random.choice(lines)
    if not mysong or mysong == '\n':
       mysong = getsong()
    return mysong	
	
def getplaylist(query):
	if query == 'party':
		myplaylist = party
	elif query =='friday':
		myplaylist = friday
	else:
		myplaylist = party
    return myplaylist	
