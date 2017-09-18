import sopel.module
import requests
import os
from xml.dom import minidom
from fake_useragent import UserAgent
from os.path import exists

script_dir = os.path.dirname(__file__)
rel_path = "swContestsLastBuild.txt"
abs_file_path = os.path.join(script_dir, rel_path)

@sopel.module.interval(60)
def getSWContests(bot):
    for channel in bot.channels:
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
                link = links[2].childNodes[0].nodeValue.split("?")[0]
                bot.msg(channel, "A new Spiceworks Contest is available!")
	        bot.msg(channel, "Title: " + title)
	        bot.msg(channel, "Link: " + link)

@sopel.module.commands('swcontests','swcontest')
def manual(bot,trigger):
    bot.say("Here is the link to the Contests Page:     https://community.spiceworks.com/fun/contests")
	
def checkLastBuildDate(xmldoc):
    lastBuildFile = os.getcwd() + abs_file_path
    lastBuildXML = xmldoc.getElementsByTagName('pubDate')
    lastBuildXML = lastBuildXML[0].childNodes[0].nodeValue
    lastBuildXML = str(lastBuildXML)

    if exists(lastBuildFile):
		#f = open(lastBuildFile, 'w+')
		#lastBuildTxt = f.Read()
		infile = open(lastBuildFile,'r')
		lastBuildTxt = str(infile.readlines()[:1])
		lastBuildTxt = lastBuildTxt.replace("'","")
		lastBuildTxt = lastBuildTxt.replace("[","")
		lastBuildTxt = lastBuildTxt.replace("]","")
		infile.close()
		if lastBuildXML.strip() != lastBuildTxt.strip():
			newContest = True
			#f.Write(lastBuildXML)
			#f.Close()
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
