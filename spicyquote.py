import sopel.module
import urllib2
from BeautifulSoup import BeautifulSoup

@sopel.module.commands('spicyquote')
def spicyQuote(bot,trigger):
    qNum = str(trigger.group(2))
    if qNum != "None":
        quote = getQuote(query)
        if quote != "Quote " + qNum + '; Invalid quote!':        
            bot.say('Spicy quote #' + qNum + ' coming up!')
            bot.say(quote)
        else:
            bot.say('There is not a quote #' + qNum + '!')
    else:
        bot.say('Please provide a quote number and try again!')




def getQuote(query):
    urlsuffix = 'http://spice.dussed.com/?'
    if query.isdigit():
        quotenum = qNum
        url = urlsuffix + qNum
    else:
        #
    soup = BeautifulSoup(urllib2.urlopen(url).read())
    txt = soup.find('td',{'class':'body'}).text
    txt = txt.replace("&lt;","<")
    txt = txt.replace("&gt;",">")
    quote = txt
    return quote

