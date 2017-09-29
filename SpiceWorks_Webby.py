import sopel.module
import requests
from lxml import html
import datetime
from time import strptime
from dateutil import parser
from dateutil.relativedelta import relativedelta

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
        bot.say(webbytimeuntil + '     Title: ' + webbytitle + '     Link: ' + webbylink)
        bot.say('BONUS: ' + webbybonus)

@sopel.module.interval(60)
def webbyauto(bot):
    page = requests.get(url,headers = None)
    if page.status_code == 200:
        for channel in bot.channels:
            now = datetime.datetime.utcnow()
            webbytime = getwebbytime()
            if str(now.month) == str(webbytime.month) and str(now.day) == str(webbytime.day):
                if str(now.hour) == str(int(webbytime.hour) - 1) and str(now.minute) == '45':
                    webbybonus = getwebbybonus()
                    webbytitle = getwebbytitle()
                    webbylink = getwebbylink()
                    bot.msg(channel, '[15 Minute Webby Reminder]     Title: ' + str(webbytitle) + '     Link: ' + str(webbylink))
                    if str(webbybonus) != '[]' or str(webbybonus) != '' or str(webbybonus) != ' ':
                        bot.msg(channel, str(webbybonus))

def getwebbytime():
    now = datetime.datetime.utcnow()
    tree = gettree()
    webbytime = str(tree.xpath('//*[@id="primary"]/div/ul/li[1]/div[1]/div[2]/span[@title]/@datetime'))
    for r in (("['", ""), ("']", "")):
        webbytime = webbytime.replace(*r)
    webbytime = str(webbytime.split("+", 1)[0])
    webbytime = parser.parse(webbytime)
    return webbytime

def getwebbytitle():
    tree = gettree()
    webbytitle = str(tree.xpath('//*[@id="primary"]/div/ul/li[1]/div[2]/h1/a/text()'))
    for r in (("['", ""), ("']", "")):
        webbytitle = webbytitle.replace(*r)
    return webbytitle

def getwebbylink():
    tree = gettree()
    webbylink = str(tree.xpath('//*[@id="primary"]/div/ul/li[1]/div[2]/h1/a/@href'))
    for r in (("['", ""), ("']", "")):
        webbylink = webbylink.replace(*r)
    webbylink = str(webbylink.split("&", 1)[0])
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
    
    if str(webbytime.year) == str(now.year):
        timetilyears = '0'
    else:
        timetilyears = str(int(webbytime.year) - int(now.year))
    
    if str(webbytime.month) == str(now.month):
        timetilmonths = '0'
    else:
        if str(timetilyears) > '0':
            timetilyears = str(int(timetilyears) - 1)
        timetilmonths = str(int(webbytime.month) - int(now.month))
    
    if str(webbytime.day) == str(now.day):
        timetildays = '0'
    else:
        if str(timetilmonths) > '0':
            timetilmonths = str(int(timetilmonths) - 1)
        if str(webbytime.day) > str(now.day):
            timetildays = str(int(webbytime.day) - int(now.day))
        else:
            daysthismonth = datetime(now.year,now.month,1)+relativedelta(months=1,days=-1)
            timetildays = str(int(daysthismonth) - int(now.day) + int(webbytime.day))

    if str(webbytime.hour) == str(now.hour):
        timetilhours = '0'
    else:
        if str(timetildays) > '0':
            timetildays = str(int(timetildays) - 1)
        if str(webbytime.hour) > str(now.hour):
            timetilhours = str(int(webbytime.hour) - int(now.hour))
        else:
            timetilhours = str(24 - int(now.hour) + int(webbytime.hour))

    if str(now.minute) == '0':
        timetilminutes = '0'
    else:
        if str(timetilhours) > '0':
            timetilhours = str(int(timetilhours) - 1)
        timetilminutes = str(60 - int(now.minute))

    if timetilyears == '0':
        timetilyears = ''
    elif timetilyears > '1':
        timetilyears = str(timetilyears + ' days ')
    else:
        timetilyears = str(timetilyears + ' day ')
        
    if timetilmonths == '0':
        timetilmonths = ''
    elif timetilmonths > '1':
        timetilmonths = str(timetilmonths + ' days ')
    else:
        timetilmonths = str(timetilmonths + ' day ')
        
    if timetildays == '0':
        timetildays = ''
    elif timetildays > '1':
        timetildays = str(timetildays + ' days ')
    else:
        timetildays = str(timetildays + ' day ')

    if timetilhours == '0':
        timetilhours = ''
    elif timetilhours > '1':
        timetilhours = str(timetilhours + ' hours ')
    else:
        timetilhours = str(timetilhours + ' hour ')

    if timetilminutes == '0':
        timetilminutes = ''
    elif timetilminutes > '1':
        timetilminutes = str(timetilminutes + ' minutes ')
    else:
        timetilminutes = str(timetilminutes + ' minute ')

    timetilwebby = str(timetilyears + timetilmonths + timetildays + timetilhours + timetilminutes)
   
    webbytimeuntil = str(timetilwebby)
    return webbytimeuntil

def gettree():
    page = requests.get(url,headers = None)
    tree= html.fromstring(page.content)
    return tree
