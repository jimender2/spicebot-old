import sopel.module
import random
import sys
import os
import html2text
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)

from SpicebotShared import *

@sopel.module.commands('xkcd','comic')
def mainfunction(bot, trigger):
  enablestatus = spicebot_prerun(bot, trigger)
  if not enablestatus:
    execute_main(bot, trigger)
    
def execute_main(bot, trigger):
  maxcomics=getmaxnumber()
  if not int(maxcomics)<=1:
    maxcomics = 1918
  if not trigger.group(2):
    mynumber =  getnumber()
  else:
    mynumber = trigger.group(2)
  if mynumber = str('today'):
    mynumber=maxcomics	
  if not  mynumber<= int(maxcomics) and mynumber>=1:
    mynumber= getnumber()      
  else:
    mynumber = getnumber()
		
  bot.say('https://xkcd.com/' + str(mynumber))
   
def getmaxnumber():
  url = 'http://xkcd.com/{}/info.0.json'.format(number)
  data = requests.get(url, verify=verify_ssl).json()
  data['url'] = 'http://xkcd.com/' + str(data['num'])
	return data
   
def getnumber():
  thenumber = random.randint(0,int(maxcomics))
  if not thenumber or thenumber == '\n':
    thenumber=getnumber()
  return thenumber
