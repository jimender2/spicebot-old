import sopel.module
import requests
from lxml import html
import datetime
from time import strptime
from dateutil import parser

url = 'https://community.spiceworks.com/calendar'

@sopel.module.commands('spicewebby')
def webbymanual(bot, trigger):
    page = requests.get(url,headers = None)
    if page.status_code == 200:
        now = datetime.datetime.utcnow()
        webbytimeuntil = getwebbytimeuntil()
        webbybonus = getwebbybonus()
        webbytitle = getwebbytitle()
        webbylink = getwebbylink()
        bot.say(webbytimeuntil + ' Until     Title: ' + webbytitle + '     Link: ' + webbylink)
        bot.say(webbybonus)


@sopel.module.interval(60)
def webbyauto(bot):
    for channel in bot.channels:
        now = datetime.datetime.utcnow()
        webbytime = getwebbytime()
        if str(now.month) == str(webbytime.month):
            if str(now.day) == str(webbytime.day):
                if str(now.hour) == str(int(webbytime.hour) - 1):
                    if now.minute == '45':
                        webbybonus = getwebbybonus()
                        webbytitle = getwebbytitle()
                        webbylink = getwebbylink()
                        bot.msg(channel, '[15 Minute Webby Reminder]     Title: ' + str(webbytitle) + '     Link: ' + str(webbylink))
                        bot.msg(channel, str(webbybonus))

def getwebbytime():
    now = datetime.datetime.utcnow()
    tree = gettree()
    webbytime = str(tree.xpath('//*[@id="primary"]/div/ul/li[1]/div[1]/div[2]/span/text()'))
    for r in (("['", ""), ("']", "")):
        webbytime = webbytime.replace(*r)
    webbyyear = str(str(str(webbytime.split(" ", 1)[1]).split(" ", 1)[1]).split(" ", 1)[0])
    webbymonth = str(webbytime.split(" ", 1)[0]).replace("['","")
    webbyday = str(webbytime.split(" ", 1)[1]).split(",", 1)[0]
    webbyhour = str(webbytime.split("at  ", 1)[1]).split(":", 1)[0]
    webbytime = str(webbymonth + ' ' + webbyday + ' ' + webbyyear + ' ' + webbyhour + ':00PM')
    webbytime = parser.parse(webbytime)
    return webbytime

def getwebbytitle():
    tree = gettree()
    webbytitle = str(tree.xpath('//*[@id="primary"]/div/ul/li[1]/div[2]/h1/a/text()'))
    for r in (("['", ""), ("']", "")):
        webbytitle = webbytitle.replace(*r)
    return webbytitle

def getwebbylink():
    webbylink = 'https://goo.gl/SsAhv'
    return webbylink

def getwebbybonus():
    tree = gettree()
    webbybonus = str(tree.xpath('//*[@id="primary"]/div/ul/li[1]/div[2]/div[2]/p/text()'))
    webbybonus = str(webbybonus.split("BONUS: ", 1)[1])
    for r in (("\\r", ""), ("\\n", ""), ("]",""), ('"',''), (" '","")):
        webbybonus = webbybonus.replace(*r)
    return webbybonus

def getwebbytimeuntil():
    now = datetime.datetime.utcnow()
    webbytime = getwebbytime()
    
    if int(now.hour) < int(webbytime.hour):
        hourcompare = str(int(webbytime.hour) - int(now.hour))
    else:
        hourcomparea = str(24 - int(now.hour))
        hourcompare = str(int(webbytime.hour) + int(hourcomparea))
    
    if int(now.minute) != '0':
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
    
    webbytimeuntilfull = str(hours) + ' ' + str(minutes)
    webbytimeuntil = str(webbytimeuntilfull)
    return webbytimeuntil

def gettree():
    page = requests.get(url,headers = None)
    tree= html.fromstring(page.content)
    return tree
