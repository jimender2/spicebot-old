import sopel.module
import random
import sys
import os
import html2text
import requests
import re
import urllib2
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)


from SpicebotShared import *
ignored_sites = [
    # For google searching
    'almamater.xkcd.com',
    'blog.xkcd.com',
    'blag.xkcd.com',
    'forums.xkcd.com',
    'fora.xkcd.com',
    'forums3.xkcd.com',
    'store.xkcd.com',
    'wiki.xkcd.com',
    'what-if.xkcd.com',
]
sites_query = ' site:xkcd.com -site:' + ' -site:'.join(ignored_sites)


@sopel.module.commands('xkcd','comic')
def mainfunction(bot, trigger):
	enablestatus = spicebot_prerun(bot, trigger)
	if not enablestatus:
		execute_main(bot, trigger)
    
def execute_main(bot, trigger):
	verify_ssl = bot.config.core.verify_ssl
	latest=get_info(verify_ssl=verify_ssl)
	maxcomics=latest['num']
	#if not int(maxcomics)<=1:
		#maxcomics = 1918
	if not trigger.group(2):
		mynumber =  getnumber(maxcomics)
	else:
		data = trigger.group(2).strip()
		if data.isdigit():
			mynumber=int(data)
		else:
			data.lower()
			if (data == 'today' or data=='latest' or data=='new'):
				mynumber=maxcomics
			elif (data == 'first' or data=='oldest'):
				mynumber = 1
			elif data == 'random':
				mynumber = getnumber(maxcomics)							
	  		else:
				bot.say('Let me find a' + data)
				baseurl = 'http://www.google.com/search?q=' + data + ' site:xkcd.com' + '&btnI'				
				bot.say(urllib2.urlopen(baseurl))
				mynumber = 1
	if not mynumber<= int(maxcomics) and mynumber>=1:
		bot.say('Please enter a number between 1 and ' +str(maxcomics))
		mynumber = maxcomics
			
	bot.say('https://xkcd.com/' + str(mynumber))
   
def get_info(number=None, verify_ssl=True):
	if number:
		url = 'http://xkcd.com/{}/info.0.json'.format(number)
	else:
		url = 'http://xkcd.com/info.0.json'
	data = requests.get(url, verify=verify_ssl).json()
	data['url'] = 'http://xkcd.com/' + str(data['num'])
	return data
   
def getnumber(maxcomics):
	thenumber = random.randint(0,int(maxcomics))
	if not thenumber or thenumber == '\n':
		thenumber=getnumber()
	return thenumber
