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
def mainfunction(bot, trigger):

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

    query = spicemanip(bot, botcom.triggerargsarray, 0) or None
    if not query:
        return osd(bot, botcom.channel_current, 'say', "Please provide a quote number or search term and try again!")

    quote = getQuote(bot, query)
    osd(bot, botcom.channel_current, 'say', quote)


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
    for link in soup.findAll('a'):
        link = link.get('href')
        if str(link).startswith("./?"):
            link = link.replace(".", "http://spice.dussed.com")
            links.append(link)
    if links == []:
        if query.isdigit():
            return "Specified quote number is not valid!"
        else:
            return "No Quotes matched " + str(query) + "!"

    # if number searched, random doesn't really do anything
    quotelink = spicemanip(bot, links, 'random')

    soup = BeautifulSoup(urllib2.urlopen(quotelink).read())
    quote = soup.find('td', {'class': 'body'}).text
    quote = unescape((anyOpenTag | anyCloseTag).suppress().transformString(quote), {"&apos;": "'", "&quot;": '"', "&nbsp;": " "})

    if len(quote) > 200:
        quote = 'That is a long quote! Here is the link: ' + quotelink

    return quote
