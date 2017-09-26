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

@sopel.module.interval(60)
def getpackt(bot):
    for channel in bot.channels:
        now = datetime.datetime.now()
        bot.msg(channel, 'testing')
        if now.hour == 14 and now.minute == 28:
            title = getPacktTitle()
            bot.msg(channel, 'Packt Free Book (daily)     https://www.packtpub.com/packt/offers/free-learning')
            bot.msg(channel, "Today's free book is: " + title)
        else:
            bot.msg(channel, now + ' is not time')

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
