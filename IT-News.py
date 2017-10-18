import sopel.module
import requests
from xml.dom import minidom
from fake_useragent import UserAgent

## If Following Template
feedname = "iT News"
url = 'https://www.itnews.com.au/RSS/rss.ashx'
alt_url = 'https://www.itnews.com.au'
## End Of Template

## Based On Template
messagestring = str("[" + feedname + "] ")
trimmedname = feedname.replace(" ","").lower
maincommand = str(trimmedname)
resetcommand = str("'" + maincommand + 'reset' + "'")
maincommand = str("'" + maincommand + "'")
lastbuilddatabase = str(maincommand + '_lastbuildcurrent')

## user agent and header
ua = UserAgent()
header = {'User-Agent': str(ua.chrome)}

## Automatic Run
@sopel.module.interval(60)
def autocheck(bot):
    for channel in bot.channels:
        page = requests.get(url, headers=header)
        if page.status_code == 200:
            title, link = checkfornew(bot, page)
            bot.msg(channel, messagestring + title + ': ' + link)

@sopel.module.rate(120)
@sopel.module.commands(maincommand)
def manualCheck(bot,trigger):
    instigator = trigger.nick
    target = trigger.nick
    update_usertotal(bot, target)
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
    	page = requests.get(url, headers=header)
	try:
	    title, link = checkfornew(bot, page)
	except TypeError:
	    title = feedname
	    link = alt_url
        bot.say(messagestring + title + ': ' + link)  
    else:
        instigator = trigger.nick
        warned = bot.db.get_nick_value(target, 'spicebothour_warn') or 0
        if not warned:
            bot.notice(target + ", you have to run .spiceboton to allow her to listen to you.", instigator)
        else:
            bot.notice(target + ", it looks like your access to spicebot has been disabled for a while. Check out ##SpiceBotTest.", instigator)

def checkfornew(bot, page):
    xml = page.text
    xml = xml.encode('ascii', 'ignore').decode('ascii')
    xmldoc = minidom.parseString(xml)
    newcontent = checkLastBuildDate(bot, xmldoc)
    if newcontent == True:
	titles = xmldoc.getElementsByTagName('title')
        title = titles[2].childNodes[0].nodeValue
        links = xmldoc.getElementsByTagName('link')
        link = links[2].childNodes[0].nodeValue.split("?")[0]
        return title, link
	
def checkLastBuildDate(bot, xmldoc):
    lastBuildXML = xmldoc.getElementsByTagName('pubDate')
    lastBuildXML = lastBuildXML[0].childNodes[0].nodeValue
    lastBuildXML = str(lastBuildXML)
    lastbuildcurrent = get_lastbuildcurrent(bot, lastBuildXML)
    if lastbuildcurrent:
	if lastBuildXML.strip() == lastbuildcurrent.strip():
	    newcontent = False
        else:
            newcontent = True
    else:
        newcontent = True
    set_lastbuildcurrent(bot, lastBuildXML)
    return newcontent

@sopel.module.require_admin
@sopel.module.commands(resetcommand)
def reset(bot,trigger):
    for channel in bot.channels:
    	bot.say('Resetting LastBuildTime...')
    	bot.db.set_nick_value(channel, lastbuilddatabase, '')

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable

def update_usertotal(bot, nick):
    usertotal = bot.db.get_nick_value(nick, 'spicebot_usertotal') or 0
    bot.db.set_nick_value(nick, 'spicebot_usertotal', usertotal + 1)

def get_lastbuildcurrent(bot, lastBuildXML):
    for channel in bot.channels:
        lastbuildcurrent = bot.db.get_nick_value(channel, lastbuilddatabase) or 0
    return lastbuildcurrent

def set_lastbuildcurrent(bot, lastbuildcurrent):
    for channel in bot.channels:
        bot.db.set_nick_value(channel, lastbuilddatabase, lastbuildcurrent)

