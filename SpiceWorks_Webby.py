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
            else:
                bot.say('stay tuned')

#@sopel.module.interval(60)
#def webbyauto(bot):
    #for channel in bot.channels:
        #now = datetime.datetime.utcnow()
        #webbyhour = getwebbyhour()
        #if now.hour == webbyhour:
            #if now.minute == '45'
                #webbytitle = getwebbytitle()
                #webbylink = getwebbylink()
                #webbybonus = getwebbybonus()
                #bot.msg(channel, webbybonus)
            
#def getwebbyhour():
    ## Parse The hour
    # return webbyhour

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
