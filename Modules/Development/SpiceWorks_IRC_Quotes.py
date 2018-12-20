#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel.module


# imports for system and OS access, directories
import os
import sys

# imports based on THIS file
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# Ensure Encoding
reload(sys)
sys.setdefaultencoding('utf-8')

comdict = {
            "author": "deathbybandaid",
            "contributors": [],
            "description": "",
            'privs': [],
            "example": "",
            "exampleresponse": "",
            }


@sopel.module.commands('spicyquote', 'spicequote')
def mainfunctionnobeguine(bot, trigger):

    botcom = bot_module_prerun(bot, trigger)
    if not botcom.modulerun:
        return

    if not botcom.multiruns:
        execute_main(bot, trigger, botcom)
    else:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, botcom.triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            botcom.triggerargsarray = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, botcom)

    botdict_save(bot)


def execute_main(bot, trigger, botcom):

    query = trigger.group(2)
    if query:
        quote = getQuote(bot, query)
        if 'Invalid quote' not in quote:
            if 'http://spice.dussed.com' in quote:
                osd(bot, trigger.sender, 'say', 'That is a long quote! Here is the link: ' + quote)
            else:
                osd(bot, trigger.sender, 'say', quote)
        else:
            osd(bot, trigger.sender, 'say', "I can't seem to find that quote! Are you sure it exists?")
    else:
        osd(bot, trigger.sender, 'say', "Please provide a quote number or search term and try again!")


def getQuote(bot, query):

    quote = None

    url = 'http://spice.dussed.com/?'

    if query.isdigit():
        url = url + query
    else:
        url = url + 'do=search&q=' + query

    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)

    links = []
    testing = 5
    for link in soup.findAll('a'):
        link = link.get('href')
        if str(link).startswith("./?"):
            testing = testing - 1
            if testing > 0:
                link = link.replace(".", "http://spice.dussed.com")
                links.append(link)
    if links == []:
        if query.isdigit():
            return "Specified quote number is not valid!"
        else:
            return "No Quotes matched " + str(query) + "!"

    # if number searched, random doesn't really do anything
    quote = spicemanip(bot, links, 'random')

    return quote

    # unescape_xml_entities = lambda s: unescape(s, {"&apos;": "'", "&quot;": '"', "&nbsp;": " "})
    # stripper = (anyOpenTag | anyCloseTag).suppress()

    if url == '':
        txt = "Invalid quote"
        return txt
    soup = BeautifulSoup(urllib2.urlopen(url).read())
    txt = soup.find('td', {'class': 'body'}).text
    txt = unescape_xml_entities(stripper.transformString(txt))
    if len(txt) > 200:
        quote = url
    else:
        quote = txt
    return quote
