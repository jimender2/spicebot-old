#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import ConfigParser
import requests
import urllib2
import json
from BeautifulSoup import BeautifulSoup
from random import randint
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
gifshareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(gifshareddir)
from BotShared import *
from GifShared import *

# creds
config = ConfigParser.ConfigParser()
config.read("/home/spicebot/spicebot.conf")


"""
Giphy
"""

giphyapi = config.get("giphy", "apikey")
giphylimit = 50


def getGif_giphy(bot, query, searchnum):
    url = 'http://api.giphy.com/v1/gifs/search?q=' + str(query)+'&api_key=' + str(giphyapi) + '&limit=' + str(giphylimit) + '&rating=r'
    data = json.loads(urllib2.urlopen(url).read())
    resultsamount = data['pagination']['total_count']
    bot.say(str(resultsamount))
    # osd(bot, 'deathbybandaid', 'say', str(data))
    try:
        id = data['data'][searchnum]['id']
        gif = 'https://media2.giphy.com/media/'+id+'/giphy.gif'
    except IndexError:
        gif = ""
    return gif


"""
Tenor
"""

tenorapi = config.get("giphy", "apikey")
tenorlimit = 5


def getGif_tenor(bot, query, searchnum):

    # load the user's anonymous ID from cookies or some other disk storage
    anon_id = get_database_value(bot, 'tenoranon', 'anon_id')
    if not anon_id:
        r = requests.get("https://api.tenor.com/v1/anonid?key=%s" % tenorapi)
        if r.status_code == 200:
            anon_id = json.loads(r.content)["anon_id"]
            set_database_value(bot, 'tenoranon', 'anon_id', anon_id)
        else:
            anon_id = ""

    # get the top 8 GIFs for the search term
    r = requests.get(
        "https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s&anon_id=%s" % (query, tenorapi, tenorlimit, anon_id))

    if r.status_code == 200:
        top_gifs = json.loads(r.content)
    else:
        top_gifs = None
    return top_gifs
