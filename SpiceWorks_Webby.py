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
        if trigger.group(2):
            if trigger.group(2) == 'time':
                webbytime = getwebbytime()
                bot.say(str(webbytime.hour))
            else:
                normalrun='true'
        else:
            normalrun='true'
    try:
        if normalrun:
            webbybonus = getwebbybonus()
            webbytitle = getwebbytitle()
            webbylink = getwebbylink()
            bot.say(webbytitle + '     Link: ' + webbylink)
            bot.say(webbybonus)
    except UnboundLocalError:
        return

#@sopel.module.interval(60)
#def webbyauto(bot):
    #for channel in bot.channels:
        #now = datetime.datetime.utcnow()
        #bot.msg(channel, '[15 Minute Webby Reminder]     Title: ' + str(webbytitle) + '     Link: ' + str(webbylink))
        #bot.msg(channel, str(webbybonus))

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

def gettree():
    page = requests.get(url,headers = None)
    tree= html.fromstring(page.content)
    return tree
