import sopel.module
import urllib2
from BeautifulSoup import BeautifulSoup
from random import randint
from pyparsing import anyOpenTag, anyCloseTag
from xml.sax.saxutils import unescape as unescape

@sopel.module.commands('spicyquote')
def spicyQuote(bot,trigger):
    query = str(trigger.group(2))
    if query != "None":
        quote = getQuote(query)
        if 'Invalid quote' not in quote:
            #bot.say('Spicy quote #' + qNum + ' coming up!')
            bot.say(quote)
        else:
            bot.say('Could not find that quote!')
    else:
        bot.say('Please provide a quote number and try again!')




def getQuote(query):
    unescape_xml_entities = lambda s: unescape(s, {"&apos;": "'", "&quot;": '"', "&nbsp;":" "})
    stripper = (anyOpenTag | anyCloseTag).suppress()
    urlsuffix = 'http://spice.dussed.com/?'
    if query.isdigit():
        qNum = query
        url = urlsuffix + qNum
    else:
        #someday we can have this check against the db and see if it is a known user.
        url = urlsuffix + 'do=search&q=' + query
        print(url)
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        links = []
        qlinks = []
        for link in soup.findAll('a'):
			links.append(link.get('href'))
        for qlink in links:
            if str(qlink).startswith("./?"):
				link = qlink.replace(".","http://spice.dussed.com")
				qlinks.append(link)
        try:
            randno = randint(1,len(qlinks))
            url = qlinks[randno]   	
        except ValueError:
            url = ""
    try:
        soup = BeautifulSoup(urllib2.urlopen(url).read())
        txt = soup.find('td',{'class':'body'}).text
        txt = txt.replace("&lt;","<")
        txt = txt.replace("&gt;",">")
        txt = unescape_xml_entities(stripper.transformString(txt))
    except:
        txt = "Invalid quote"
    quote = txt
    return quote

