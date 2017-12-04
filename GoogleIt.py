import sopel.module
import random
import sys
import os
import requests
import urllib2

moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)

from SpicebotShared import *

@sopel.module.commands('google','googleit')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray)
    
def execute_main(bot, trigger, triggerargsarray):
  if not trigger.group(2):
    bot.say('Please enter a term to search for')
  else:
    data = trigger.group(2).strip()
    data.lower()
    data=data.replace(' ', '%20').replace('site:', 'site%3A')
    #data=data.replace('site:', 'site%3A')
    var = requests.get(r'http://www.google.com/search?q=' + data + '&btnI')
    bot.say(str(var.url))	
