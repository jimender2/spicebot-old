import sopel.module
import random
import urllib
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

party='https://raw.githubusercontent.com/deathbybandaid/SpiceBot/master/Text-Files/jukebox_party.txt'
friday='https://raw.githubusercontent.com/deathbybandaid/SpiceBot/master/Text-Files/jukebox_friday.txt'

@sopel.module.commands('dj')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
	if not trigger.group(2):
		playlist=party
	else:
		query = trigger.group(2).replace(' ','20%')
		query = str(query)
		playlist = getplaylist(query)
		if playlist == party:
			bot.say('You have selected the Party Playlist')		
	song = getsong(playlist)
	if song:
		bot.say(trigger.nick + ' puts a nickel in the jukebox and it starts to play ' + song)
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
