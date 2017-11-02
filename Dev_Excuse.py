import sopel.module
import urllib
from xml.dom.minidom import parseString
import sys
import os
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

@sopel.module.commands('devexcuse')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    bot.say(parseString(
        urllib.urlopen('http://developerexcuses.com').read().replace('&', '')).
        getElementsByTagName('body')[0].getElementsByTagName('div')[0].
        getElementsByTagName('center')[0].getElementsByTagName('a')[0].
        childNodes[0].nodeValue)
