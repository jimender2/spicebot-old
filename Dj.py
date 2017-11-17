import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('dj')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    song = getsong()
    if song:
        bot.say(song)
    else:
        bot.say('Never Gonna Give You Up by Rick Astley')

def getsong():
    #url replace with a song API
    #url = 'https://icanhazdadjoke.com'    
    #page = requests.get(url,headers = {'Accept':'text/plain'}) 
    #song = page.content
    song='Party all the Time by Eddie Murphy '
    return song
