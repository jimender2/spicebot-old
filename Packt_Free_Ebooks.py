import sopel.module
import requests
from lxml import html
from fake_useragent import UserAgent
from datetime import datetime, timedelta
import datetime
import arrow
import time

# new book is 23:00 UTC
packthour = str(23)
packtminute = str(10)

@sopel.module.interval(60)
def getpackt(bot):
    for channel in bot.channels:
        now = datetime.datetime.utcnow()
        if now.hour == int(packthour) and now.minute == int(packtminute):
            title = getPacktTitle()
            packttimediff = getpackttimediff()
            bot.msg(channel, "Packt Free Book Today is: " + title + '     Time Left: ' + str(packttimediff) + '     URL: https://www.packtpub.com/packt/offers/free-learning')

@sopel.module.rate(120)
@sopel.module.commands('packt')
def packt(bot, trigger):
    packttimediff = getpackttimediff()
    if trigger.group(2):
        if trigger.group(2) == 'time':
            bot.say('Time Left: ' + str(packttimediff))
        else:
            normalrun='true'
    else:
        normalrun='true'
    try:
        if normalrun:
            title = getPacktTitle()
            bot.say("Packt Free Book Today is: " + title + '     Time Left: ' + str(packttimediff) + '     URL: https://www.packtpub.com/packt/offers/free-learning')
    except UnboundLocalError:
        return

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
    now = datetime.datetime.utcnow()
    packtnext = None
    if now.hour < packthour:
        packtnext = datetime.datetime(now.year, now.month, now.day, 23, 0, 0, 0)
        #packtnext = datetime.(now.year, now.month, now.day, str(packthour), str(packtminute), 0, 0)
    else:
        day = timedelta(days=1)
        tomorrow = now + day
        packtnext = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 23, 0, 0, 0)
        #packtnext = datetime.(tomorrow.year, tomorrow.month, tomorrow.day, packthour, packtminute, 0, 0)
    a = arrow.get(now)
    b = arrow.get(packtnext)
    timecompare = (b.humanize(a, granularity='auto'))
    packttimediff = str(packttimedifffull)
    return packttimediff
