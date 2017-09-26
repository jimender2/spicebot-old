import sopel.module
import requests
from lxml import html
from fake_useragent import UserAgent
import time

@sopel.module.rate(120)
@sopel.module.commands('packt')
def packt(bot, trigger):
    title = getPacktTitle()
    bot.say('Packt Free Book (daily)     https://www.packtpub.com/packt/offers/free-learning')
    bot.say("Today's free book is: " + title)

@sopel.module.interval(60)
def getpackt(bot):
    now = datetime.now()
    now_time = now.time()
    for channel in bot.channels:
        if now_time == time(13,50):
            title = getPacktTitle()
            bot.say('Packt Free Book (daily)     https://www.packtpub.com/packt/offers/free-learning')
            bot.say("Today's free book is: " + title)

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
