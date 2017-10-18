import sopel.module
import requests
import os
from xml.dom import minidom
from fake_useragent import UserAgent
from os.path import exists

script_dir = os.path.dirname(__file__)
rel_path = "data/swContestsLastBuild.txt"
abs_file_path = os.path.join(script_dir, rel_path)
url = 'https://community.spiceworks.com/feed/forum/1550.rss'
ua = UserAgent()
header = {'User-Agent': str(ua.chrome)}
	
@sopel.module.interval(60)
def getSWContests(bot):
    for channel in bot.channels:
        page = requests.get(url, headers=header)
        if page.status_code == 200:
            title, link = checkfornew(bot, page)
            bot.msg(channel, "[Spiceworks Contest] " + title + ": " + link)

def checkfornew(bot, page):
    xml = page.text
    xml = xml.encode('ascii', 'ignore').decode('ascii')
    xmldoc = minidom.parseString(xml)
    newContest = checkLastBuildDate(xmldoc)
    if newContest == True:
	titles = xmldoc.getElementsByTagName('title')
        title = titles[2].childNodes[0].nodeValue
        links = xmldoc.getElementsByTagName('link')
        link = links[2].childNodes[0].nodeValue.split("?")[0]
	return title, link

@sopel.module.rate(120)
@sopel.module.commands('swcontests','spicecontests')
def manualCheck(bot,trigger):
    instigator = trigger.nick
    target = trigger.nick
    update_usertotal(bot, target)
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
    	page = requests.get(url, headers=header)
    	if page.status_code == 200:
	    try:
	        title, link = checkfornew(bot, page)
	    except TypeError:
		return
	    if title and link:
                bot.say("[Spiceworks Contest] " + title + ": " + link)
	    else:
		bot.say("Contests Page: https://community.spiceworks.com/fun/contests")
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
			newContest = True
			outfile = open(lastBuildFile,'w')
			outfile.write(lastBuildXML)
			outfile.close()
		else:
			newContest = False
    else:		
		outfile = open(lastBuildFile,'w')
		outfile.write(lastBuildXML)
		outfile.close()
		newContest = True
    return newContest

@sopel.module.require_admin
@sopel.module.commands('swcontestsreset','spiceconteststreset')
def reset(bot,trigger):
    	bot.say('Removing Last Build File...')
    	os.system("sudo rm " + abs_file_path)

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
