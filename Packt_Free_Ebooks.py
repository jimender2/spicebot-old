import sopel.module
import requests
from lxml import html
from fake_useragent import UserAgent
import datetime

@sopel.module.rate(120)
@sopel.module.commands('packt')
def packt(bot, trigger):
    title = getPacktTitle()
    bot.say('Packt Free Book (daily)     https://www.packtpub.com/packt/offers/free-learning')
    bot.say("Today's free book is: " + title)

# new book is 7pm EDT, 11:00 PM UTC
@sopel.module.interval(60)
def getpackt(bot):
    for channel in bot.channels:
        now = datetime.datetime.now()
        #if now.hour == 11 and now.minute == 05:
        if now.hour == 15 and now.minute == 10:
            title = getPacktTitle()
            bot.msg(channel, 'Packt Free Book (daily)     https://www.packtpub.com/packt/offers/free-learning')
            bot.msg(channel, "Today's free book is: " + str(title))

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

#def packttimediff():
    #now = datetime.datetime.now('UTC')
    #packthour = '11'
    #packtminute = '00'
    #if now.hour < packthour:
        #hourcompare = int(packthour) - int(now.hour)
        #minutecompare = int(packtminute) - int(now.hour)
