import sopel.module
import requests
from lxml import html
from fake_useragent import UserAgent
import datetime

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
    
    if int(now.hour) < int(packthour):
        hourcompare = str(int(packthour) - int(now.hour))
    else:
        hourcompare = str(packthour)
    
    if int(now.minute) > '0':
        hourcompare = str(int(hourcompare) - 1)
        minutecompare = str(60 - int(now.minute))
    else:
        hourcompare = str(hourcompare)
        minutecompare = str(60 - int(now.minute))
    
    if hourcompare == '1':
        hours = hourcompare + ' ' + 'hour'
    elif hourcompare == '0':
        hours = ''
    else:
        hours = hourcompare + ' ' + 'hours'   
    
    if minutecompare == '1':
        minutes = minutecompare + ' ' + 'minute'
    elif minutecompare == '0':
        minutes = ''
    else:
        minutes = minutecompare + ' ' + 'minutes'       
    
    packttimedifffull = str(hours) + ' ' + str(minutes)
    packttimediff = str(packttimedifffull)
    return packttimediff
