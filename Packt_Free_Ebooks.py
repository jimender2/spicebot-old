import sopel.module
import requests
from lxml import html
from fake_useragent import UserAgent
from datetime import datetime, timedelta
import datetime
import arrow
import time
import sys
import os
from datetime import datetime
from pytz import timezone
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)
from SpicebotShared import *

# new book is Midnight GMT
tz = timezone('GMT')
packthour = str(0)
packtminute = str(10)

@sopel.module.commands('packt')
def mainfunction(bot, trigger):
    enablestatus = spicebot_prerun(bot, trigger)
    if not enablestatus:
        execute_main(bot, trigger)
    
def execute_main(bot, trigger):
    packttimediff = getpackttimediff()
    if trigger.group(2):
        if trigger.group(2) == 'time':
            bot.say(str(packttimediff))
        else:
            normalrun='true'
    else:
        normalrun='true'
    try:
        if normalrun:
            title = getPacktTitle()
            bot.say("Packt Free Book Today is: " + title + str(packttimediff) + '     URL: https://www.packtpub.com/packt/offers/free-learning')
    except UnboundLocalError:
        return
    
@sopel.module.interval(60)
def getpackt(bot):
    for channel in bot.channels:
        #now = datetime.datetime.utcnow()
        now = datetime.now(tz)
        if now.hour == int(packthour) and now.minute == int(packtminute):
            title = getPacktTitle()
            packttimediff = getpackttimediff()
            bot.msg(channel, "Packt Free Book Today is: " + title +  str(packttimediff) + '     URL: https://www.packtpub.com/packt/offers/free-learning')

def getPacktTitle():
        url = 'https://www.packtpub.com/packt/offers/free-learning'

        ua = UserAgent()
        header = {'User-Agent':str(ua.chrome)}
        page = requests.get(url,headers = header)

        if page.status_code == 200:
                tree = html.fromstring(page.content)
                title = str(tree.xpath('//*[@id="deal-of-the-day"]/div/div/div[2]/div[2]/h2/text()'))
                title = title.replace("\\t","")
                title = title.replace("\\n","")
                return title
        else:
                title = 'Could not get Title. The status code was : ' + page.status_code
        return title

def getpackttimediff():
    #now = datetime.datetime.utcnow()
    now = datetime.now(tz)
    packtnext = None
    if now.hour < packthour:
        packtnext = datetime(now.year, now.month, now.day, int(packthour), int(packtminute), 0, 0)
    else:
        day = timedelta(days=1)
        tomorrow = now + day
        packtnext = datetime(tomorrow.year, tomorrow.month, tomorrow.day, int(packthour), int(packtminute), 0, 0)
    a = arrow.get(now)
    b = arrow.get(packtnext)
    timecompare = (b.humanize(a, granularity='auto'))
    packttimediff = str('     Next Book: ' + timecompare)
    return packttimediff
