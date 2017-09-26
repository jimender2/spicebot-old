import sopel.module
import requests
from lxml import html
from fake_useragent import UserAgent
import datetime

@sopel.module.rate(120)
@sopel.module.commands('packt')
def packt(bot, trigger):
    title = getPacktTitle()
    packttimediff = getpackttimediff()
    #bot.say('Packt Free Book (daily)     https://www.packtpub.com/packt/offers/free-learning')
    bot.say("Packt Free Book Today is: " + title + '     Time Left: ' + str(packttimediff) + '     URL: https://www.packtpub.com/packt/offers/free-learning')

# new book is 23:00 UTC
@sopel.module.interval(60)
def getpackt(bot):
    for channel in bot.channels:
        now = datetime.datetime.utcnow()
        if now.hour == 23 and now.minute == 10:
            title = getPacktTitle()
            packttimediff = getpackttimediff()
            #bot.msg(channel, 'Packt Free Book (daily)     https://www.packtpub.com/packt/offers/free-learning')
            bot.msg(channel, "Packt Free Book Today is: " + title + '     Time Left: ' + str(packttimediff) + '     URL: https://www.packtpub.com/packt/offers/free-learning')

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
    packthour = '23'
    if now.hour < packthour:
        packttimediff = int(packthour) - int(now.hour)
    else:
        hourcomparea = 24 - int(now.hour)
        packttimediff = int(hourcomparea) + int(packthour)
    
    if int(now.minute) > 1:
        packtminutediff = str(60 - int(now.minute))
        packttimediff = str(int(packttimediff) - 1) + ' hours ' + packtminutediff + ' minutes.'
    else:
        packttimediff = str(int(packttimediff)) + ' hours '
    return packttimediff
