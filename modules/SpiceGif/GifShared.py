#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import ConfigParser
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


def getGif_giphy(query):
    limit = 50
    url = 'http://api.giphy.com/v1/gifs/search?q=' + str(query)+'&api_key=' + str(giphyapi) + '&limit=' + str(limit) + '&rating=r'
    data = json.loads(urllib2.urlopen(url).read())
    randno = randint(0, limit)
    try:
        id = data['data'][randno]['id']
        gif = 'https://media2.giphy.com/media/'+id+'/giphy.gif'
    except IndexError:
        gif = ""
    return gif, randno


"""
Tenor
"""

tenorapi = config.get("giphy", "apikey")


def getGif_tenor(query):
    # set the apikey and limit
    apikey = "LIVDSRZULELA"  # test value
    lmt = 8

    # load the user's anonymous ID from cookies or some other disk storage
    # anon_id = <from db/cookies>

    # ELSE - first time user, grab and store their the anonymous ID
    r = requests.get("https://api.tenor.com/v1/anonid?key=%s" % apikey)

    if r.status_code == 200:
        anon_id = json.loads(r.content)["anon_id"]
        # store in db/cookies for re-use later
    else:
        anon_id = ""

    # our test search
    search_term = "excited"

    # get the top 8 GIFs for the search term
    r = requests.get(
        "https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s&anon_id=%s" % (search_term, apikey, lmt, anon_id))

    if r.status_code == 200:
        # load the GIFs using the urls for the smaller GIF sizes
        top_8gifs = json.loads(r.content)
        # print top_8gifs
    else:
        top_8gifs = None

    # continue a similar pattern until the user makes a selection or starts a new search.
