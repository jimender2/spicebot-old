import sopel.module
import requests
import os
from xml.dom import minidom
from fake_useragent import UserAgent
from os.path import exists

script_dir = os.path.dirname(__file__)
rel_path = "data/itnewslastbuild.txt"
abs_file_path = os.path.join(script_dir, rel_path)
url = 'https://www.itnews.com.au/RSS/rss.ashx?type=Category&ID=406'

@sopel.module.interval(60)
def getitnews(bot):
    for channel in bot.channels:
        ua = UserAgent()
        header = {'User-Agent': str(ua.chrome)}
        page = requests.get(url, headers=header)

    	if page.status_code == 200:
            xml = page.text
            xml = xml.encode('ascii', 'ignore').decode('ascii')
            xmldoc = minidom.parseString(xml)
            newnews = checkLastBuildDate(xmldoc)
            if newnews == True:
                titles = xmldoc.getElementsByTagName('title')
                title = titles[2].childNodes[0].nodeValue
                links = xmldoc.getElementsByTagName('link')
                link = links[2].childNodes[0].nodeValue.split("?")[0]
                bot.msg(channel, "[iT News] " + title + '     Link: ' + link)

@sopel.module.rate(120)
@sopel.module.commands('itnews')
def manualCheck(bot,trigger):
    instigator = trigger.nick
    target = trigger.nick
    update_usertotal(bot, target)
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
    	ua = UserAgent()
    	header = {'User-Agent': str(ua.chrome)}
    	page = requests.get(url, headers=header)

    	if page.status_code == 200:
            xml = page.text
            xml = xml.encode('ascii', 'ignore').decode('ascii')
            xmldoc = minidom.parseString(xml)
            newnews = checkLastBuildDate(xmldoc)
            titles = xmldoc.getElementsByTagName('title')
            title = titles[2].childNodes[0].nodeValue
            links = xmldoc.getElementsByTagName('link')
            link = links[2].childNodes[0].nodeValue.split("?")[0]
            bot.say("[iT News] " + title + '     Link: ' + link)
    else:
        instigator = trigger.nick
        warned = bot.db.get_nick_value(target, 'spicebothour_warn') or 0
        if not warned:
            bot.notice(target + ", you have to run .spiceboton to allow her to listen to you.", instigator)
        else:
            bot.notice(target + ", it looks like your access to spicebot has been disabled for a while. Check out ##SpiceBotTest.", instigator)

def update_usertotal(bot, nick):
    usertotal = bot.db.get_nick_value(nick, 'spicebot_usertotal') or 0
    bot.db.set_nick_value(nick, 'spicebot_usertotal', usertotal + 1)
	
def checkLastBuildDate(xmldoc):
    lastBuildFile = os.getcwd() + abs_file_path
    lastBuildXML = xmldoc.getElementsByTagName('pubDate')
    lastBuildXML = lastBuildXML[0].childNodes[0].nodeValue
    lastBuildXML = str(lastBuildXML)

    if exists(lastBuildFile):
		infile = open(lastBuildFile,'r')
		lastBuildTxt = str(infile.readlines()[:1])
		lastBuildTxt = lastBuildTxt.replace("'","")
		lastBuildTxt = lastBuildTxt.replace("[","")
		lastBuildTxt = lastBuildTxt.replace("]","")
		infile.close()
		if lastBuildXML.strip() != lastBuildTxt.strip():
			newnews = True
			outfile = open(lastBuildFile,'w')
			outfile.write(lastBuildXML)
			outfile.close()
		else:
			newnews = False
    else:		
		outfile = open(lastBuildFile,'w')
		outfile.write(lastBuildXML)
		outfile.close()
		newnews = True
    return newnews

@sopel.module.require_admin
@sopel.module.commands('itnewsreset')
def reset(bot,trigger):
    	bot.say('Removing Contests File...')
    	os.system("sudo rm " + abs_file_path)

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
