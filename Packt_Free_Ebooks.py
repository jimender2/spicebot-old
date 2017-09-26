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
    now = datetime.datetime.now()
    bot.say(now)
    packttimea = now.replace(hour=2, minute=16, second=0, microsecond=0)
    packttimeb = now.replace(hour=2, minute=17, second=0, microsecond=0)
    for channel in bot.channels:
        if now > packttimea and now < packttimeb:
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
