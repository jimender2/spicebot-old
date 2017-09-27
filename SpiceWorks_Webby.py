import sopel.module
import requests
from lxml import html

url = 'https://community.spiceworks.com/calendar'

@sopel.module.commands('spicewebby')
def webbymanual(bot, trigger):
    page = requests.get(url,headers = None)
    if page.status_code == 200:
        if trigger.group(2):
            if trigger.group(2) == 'bonus':
                webbybonus = getwebbybonus()
                bot.say(webbybonus)
            elif trigger.group(2) == 'title':
                webbytitle = getwebbytitle()
                bot.say(webbytitle)
            elif trigger.group(2) == 'time':
                webbymonth = getwebbymonth()
                webbyday = getwebbyday()
                webbyhour= getwebbyhour()
                webbytime = str(webbymonth + ' ' + webbyday+ ' ' + webbyhour + ':00 UTC')
                bot.say(webbytime)
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
        #!!!!!! webbymonth = getwebbymonth()
            #!!!!!! webbydate = getwebbydate()
            #!!!!!! if now.date = webbydate
                #webbyhour = getwebbyhour()
                #if now.hour == webbyhour:
                    #if now.minute == '45'
                        #webbytitle = getwebbytitle()
                        #webbylink = getwebbylink()
                        #webbybonus = getwebbybonus()
                        #bot.msg(channel, webbybonus)

def getwebbymonth():
    webbymonth = 'Sept'
    return webbymonth

def getwebbyday():
    tree = gettree()
    webbyday = str(tree.xpath('//*[@id="primary"]/div/ul/li[1]/div[1]/div[2]/span/text()'))
    webbyday = str(str(webbyday.split(" ", 1)[1]).split(",", 1)[0])
    return webbyday

def getwebbyhour():
    tree = gettree()
    webbyhour = str(tree.xpath('//*[@id="primary"]/div/ul/li[1]/div[1]/div[2]/span/text()'))
    webbyhour = str(str(webbyhour.split("at  ", 1)[1]).split(":", 1)[0])
    webbyhour = str(int(webbyhour) + 12)
    return webbyhour

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
