import sopel.module
import requests
import os
from xml.dom import minidom
from fake_useragent import UserAgent
from os.path import exists

@sopel.module.commands('swcontests')
def getSWContests(bot,trigger):
    url = 'https://community.spiceworks.com/feed/forum/1550.rss'
    ua = UserAgent()
    header = {'User-Agent': str(ua.chrome)}
    page = requests.get(url, headers=header)

    if page.status_code == 200:
        xml = page.text
        xml = xml.encode('ascii', 'ignore').decode('ascii')
        xmldoc = minidom.parseString(xml)
        newContest = checkLastBuildDate(xmldoc)
        if newContest == True:
            titles = xmldoc.getElementsByTagName('title')
            title = titles[2].childNodes[0].nodeValue
            links = xmldoc.getElementsByTagName('link')
            link = links[2].childNodes[0].nodeValue
            bot.say("A new Spiceworks Contest is available!")
            bot.say("Title: " + title + " Link: " + link)
            #print("A new Spiceworks Contest is available!")
            #print("Title: " + title + " Link: " + link)
    else:
		bot.say("Unable to reach the Spiceworks Contest Page.")


def checkLastBuildDate(xmldoc):
    lastBuildFile = os.getcwd() + "\\swContestsLastBuild.txt"
    lastBuildXML = xmldoc.getElementsByTagName('lastBuildDate')
    lastBuildXML = lastBuildXML[0].childNodes[0].nodeValue

    if exists(lastBuildFile):
		f = open(lastBuildFile, 'w+')
		lastBuildTxt = r.Read()
		if lastBuildXML != lastBuildTxt:
			newContest = True
			lastBuildFile.Write(lastBuildXML)
			lastBuildFile.Close()
		else:
			newContest = False
		else:
		f = open(lastBuildFile, 'w+')
		f.Write(lastBuildXML)
		f.Close()
		newContest = True
    return newContest
