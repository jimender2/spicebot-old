import sopel.module
import requests
from lxml import html

url = 'https://community.spiceworks.com/calendar'

@sopel.module.commands('spicewebby')
def webbymanual(bot, trigger):
    page = requests.get(url,headers = None)
    if page.status_code == 200:
        if not trigger.group(2):
            bot.say('stay tuned')
        else:
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
                bot.say('stay tuned')

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
    webbymonth = 'test'
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
    if not webbytitle:
        webbytitle = 'No title Available'
    return webbytitle

#def getwebbylink():
    ## Parse the url out,,, don't need anything after ShowKey
    #return webbylink

def getwebbybonus():
    tree = gettree()
    webbybonus = str(tree.xpath('//*[@id="primary"]/div/ul/li[1]/div[2]/div[2]/p/text()'))
    webbybonus = str(webbybonus.split("BONUS: ", 1)[1])
    for r in (("\\r", ""), ("\\n", ""), ("]",""), ('"',''), (" '","")):
        webbybonus = webbybonus.replace(*r)
    if not webbybonus:
        webbybonus = 'No Bonus Available'
    return webbybonus

def gettree():
    page = requests.get(url,headers = None)
    tree= html.fromstring(page.content)
    return tree
