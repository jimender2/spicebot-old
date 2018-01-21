#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import urllib2
from BeautifulSoup import BeautifulSoup
from random import randint
from pyparsing import anyOpenTag, anyCloseTag
from xml.sax.saxutils import unescape as unescape
import sys
import os
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from SpicebotShared import *

@sopel.module.commands('spicyquote')
def execute_main(bot, trigger):
    query = trigger.group(2)
    if query:
        quote = getQuote(query)
        if 'Invalid quote' not in quote:
            if 'http://spice.dussed.com' in quote:
                bot.say('That is a long quote! Here is the link: ' + quote)
            else:
                bot.say(quote)
        else:
            bot.say("I can't seem to find that quote! Are you sure it exists?")
    else:
        bot.say("Please provide a quote number or search term and try again!")

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
        txt = unescape_xml_entities(stripper.transformString(txt))
    except:
        txt = "Invalid quote"
    
    if len(txt) > 200:
        quote = url
    else:
        quote = txt
    return quote
