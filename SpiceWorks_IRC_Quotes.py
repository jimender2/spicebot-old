import sopel.module
import urllib2
from BeautifulSoup import BeautifulSoup
from random import randint
from pyparsing import anyOpenTag, anyCloseTag
from xml.sax.saxutils import unescape as unescape

@sopel.module.rate(120)
@sopel.module.commands('spicyquote')
def spicyQuote(bot,trigger):
    instigator = trigger.nick
    target = trigger.nick
    update_usertotal(bot, target)
    targetdisenable = get_disenable(bot, target)
    if targetdisenable:
        query = str(trigger.group(2))
        if query != "None":
            quote = getQuote(query)
            if 'Invalid quote' not in quote:
                if 'http://spice.dussed.com' in quote:
                    bot.say('That is a long quote! Here is the link: ' + quote)
                else:
                    bot.say(quote)
            else:
                bot.say('Could not find that quote!')
        else:
            bot.say('Please provide a quote number and try again!')
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
        except ValueError:
            randno = int("0")
	try:
            url = qlinks[randno]
        except IndexError:
            url = ""
    try:
        soup = BeautifulSoup(urllib2.urlopen(url).read())
        txt = soup.find('td',{'class':'body'}).text
        #txt = txt.replace("&lt;","<")
        #txt = txt.replace("&gt;",">")
        txt = unescape_xml_entities(stripper.transformString(txt))
    except:
        txt = "Invalid quote"
    
    if len(txt) > 200:
        quote = url
    else:
        quote = txt
    return quote

## Check Status of Opt In
def get_disenable(bot, nick):
    disenable = bot.db.get_nick_value(nick, 'spicebot_disenable') or 0
    return disenable
