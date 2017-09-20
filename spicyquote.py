import sopel.module
import urllib2
from BeautifulSoup import BeautifulSoup
from random import randint

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
    urlsuffix = 'http://spice.dussed.com/?'
    if query.isdigit():
        quotenum = qNum
        url = urlsuffix + qNum
    else:
        #someday we can have this check against the db and see if it is a known user.
        url = urlsuffix + 'do=search&q=' + query
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        links = []
        for link in soup.findAll('a'):
            if link.startswith('./?'):
                link = link.replace(".","http://spice.dussed.com")
                links.append(link)                            
        randno = randint(0,len(links))
        url = links[randno]                
    soup = BeautifulSoup(urllib2.urlopen(url).read())
    txt = soup.find('td',{'class':'body'}).text
    txt = txt.replace("&lt;","<")
    txt = txt.replace("&gt;",">")
    quote = txt
    return quote

