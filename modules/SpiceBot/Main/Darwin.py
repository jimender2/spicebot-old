#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import urllib2
import json
from BeautifulSoup import BeautifulSoup
from random import randint
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *


@sopel.module.commands('darwin')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    gif,randno = getGif("Darwin Award")
    if gif:
        bot.say("Result no: %s: %s" % (randno, gif))
    else:
        bot.action('is not a contender for the Darwin award, thank fuck.')


def getGif(query):
    api = 'Wi33J3WxSDxWsrxLREcQqmO3iJ0dk52N'
    limit = 50
    urlquery = query.replace(" ","%20")
    url = 'http://api.giphy.com/v1/gifs/search?q=' + str(urlquery)+'&api_key=' + str(api) + '&limit=' + str(limit) + '&rating=r'
    data = json.loads(urllib2.urlopen(url).read())
    randno = randint(0,limit)
    try:
        id = data['data'][randno]['id']
        gif = 'https://media2.giphy.com/media/'+id+'/giphy.gif'
    except IndexError:
        gif = ""
    return gif,randno
