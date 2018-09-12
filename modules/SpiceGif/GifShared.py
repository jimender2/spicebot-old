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


def getGif_giphy(bot, query, searchnum, searchlimit=giphylimit):

    returngifdict = {
                    "query": query,
                    "searchquery": query,
                    "querysuccess": False,
                    "returnnum": searchnum,
                    "returnurl": None,
                    "error": None
                    }

    # Make sure there is a valid input of query and search number
    if not query:
        returngifdict["error"] = 'No Query to Search'
        return returngifdict
    if not str(searchnum).isdigit() and searchnum != 'random':
        returngifdict["error"] = 'No Search Number or Random Specified'
        return returngifdict

    # spaces in query
    searchquery = query.replace(' ', '%20')
    returngifdict["searchquery"] = searchquery

    # Random
    if searchnum == 'random':
        searchnum = randint(0, searchlimit)

    url = 'http://api.giphy.com/v1/gifs/search?q=' + str(searchquery) + '&api_key=' + str(giphyapi) + '&limit=' + str(searchlimit) + '&rating=r'
    data = json.loads(urllib2.urlopen(url).read())

    # Verifythere are results
    resultsamount = data['pagination']['total_count']
    returngifdict["resultsamount"] = resultsamount
    if not resultsamount:
        return returngifdict
    returngifdict["querysuccess"] = True

    if int(searchnum) > int(resultsamount):
        searchnum = resultsamount
    returngifdict["returnnum"] = searchnum

    id = data['data'][searchnum]['id']
    returngifdict["returnurl"] = 'https://media2.giphy.com/media/'+id+'/giphy.gif'

    return returngifdict


"""
Tenor
"""

tenorapi = config.get("tenor", "apikey")
tenorlimit = 50


def getGif_tenor(bot, query, searchnum, searchlimit=tenorlimit):

    returngifdict = {
                    "query": query,
                    "searchquery": query,
                    "querysuccess": False,
                    "returnnum": searchnum,
                    "returnurl": None,
                    "error": None
                    }

    # Make sure there is a valid input of query and search number
    if not query:
        returngifdict["error"] = 'No Query to Search'
        return returngifdict
    if not str(searchnum).isdigit() and searchnum != 'random':
        returngifdict["error"] = 'No Search Number or Random Specified'
        return returngifdict

    # spaces in query
    searchquery = query.replace(' ', '%20')
    returngifdict["searchquery"] = searchquery

    # Random
    if searchnum == 'random':
        searchnum = randint(0, searchlimit)

    url = 'https://api.tenor.com/v1/search?q=' + str(searchquery) + '&key=' + str(tenorapi) + '&limit=' + str(searchlimit)  # + '&anon_id=r' + str(anon_id)
    data = json.loads(urllib2.urlopen(url).read())

    # Verifythere are results
    resultsamount = len(data['results'])
    if not resultsamount:
        return returngifdict
    returngifdict["querysuccess"] = True

    if int(searchnum) > int(resultsamount):
        searchnum = resultsamount
    returngifdict["returnnum"] = searchnum

    resultnum = data['results'][searchnum]['media']
    bot.say(str(resultnum))
    return

    returngifdict["returnurl"] = data['results'][searchnum]['media']['gif']['url']

    return returngifdict

    gifdictionary = {
                        'weburl': 'https://tenor.com/search/fart-gifs',
                        'results': [
                                    {
                                        'created': 1461358331.449446,
                                        'url': 'https://tenor.com/wFAJ.gif',
                                        'media': [
                                                {
                                                    'nanomp4': {
                                                                'url': 'https://media.tenor.com/videos/c3926a1bf3a1cb398d348cb5de597767/mp4',
                                                                'dims': [150, 200],
                                                                'duration': 1.1,
                                                                'preview': 'https://media.tenor.com/images/d2c2d717c743367ba5a9ee094c0587da/tenor.png',
                                                                'size': 26734
                                                                },
                                                    'nanowebm': {
                                                                'url': 'https://media.tenor.com/videos/b6583e893d984414ed3bce27119833b1/webm',
                                                                'dims': [150, 200],
                                                                'preview': 'https://media.tenor.com/images/d2c2d717c743367ba5a9ee094c0587da/tenor.png',
                                                                'size': 18585},
                                                    'tinygif': {
                                                                'url': 'https://media.tenor.com/images/3780eadf5dc84d7e614b686843d2a849/tenor.gif',
                                                                'dims': [220, 292],
                                                                'preview': 'https://media.tenor.com/images/e0ff6abe416df30c69ac7b13fff2e264/raw',
                                                                'size': 73942
                                                                },
                                                    'tinymp4': {
                                                                'url': 'https://media.tenor.com/videos/442dd4ca3166c600daff85411c33dc58/mp4',
                                                                'dims': [200, 266],
                                                                'duration': 1.037037,
                                                                'preview': 'https://media.tenor.com/images/3dc1a390e9818915801f1b0a9f8021f8/tenor.png',
                                                                'size': 56575
                                                                },
                                                    'tinywebm': {
                                                                'url': 'https://media.tenor.com/videos/e037b28a690051b26d88e516d67fb07e/webm',
                                                                'dims': [200, 266],
                                                                'preview': 'https://media.tenor.com/images/3dc1a390e9818915801f1b0a9f8021f8/tenor.png',
                                                                'size': 34031
                                                                },
                                                    'webm': {
                                                                'url': 'https://media.tenor.com/videos/f8ca3f540f3ee8cb771da87c72578545/webm',
                                                                'dims': [200, 266],
                                                                'preview': 'https://media.tenor.com/images/56b7390fdaa0b7a5ce30fadff9ebdbd7/raw',
                                                                'size': 34031
                                                                },
                                                    'gif': {
                                                                'url': 'https://media.tenor.com/images/6fbc9ef9dc3f91891e47553bc047696f/tenor.gif',
                                                                'dims': [200, 266],
                                                                'preview': 'https://media.tenor.com/images/56b7390fdaa0b7a5ce30fadff9ebdbd7/raw',
                                                                'size': 865850
                                                                },
                                                    'mp4': {
                                                                'url': 'https://media.tenor.com/videos/283be06fd38086ef012a5c176ca95b79/mp4',
                                                                'dims': [200, 266],
                                                                'duration': 1.037037,
                                                                'preview': 'https://media.tenor.com/images/56b7390fdaa0b7a5ce30fadff9ebdbd7/raw',
                                                                'size': 32955
                                                                },
                                                    'nanogif': {
                                                                'url': 'https://media.tenor.com/images/a9813b46edc256cf8a6b191167a0aee5/tenor.gif',
                                                                'dims': [67, 90],
                                                                'preview': 'https://media.tenor.com/images/ebb385b4a02abb54f101160c5565b400/raw',
                                                                'size': 7854
                                                                },
                                                    'mediumgif': {
                                                                'url': 'https://media.tenor.com/images/663bd03c3bc3457e557c21ab608d12fa/tenor.gif',
                                                                'dims': [200, 266],
                                                                'preview': 'https://media.tenor.com/images/ed3ac72ff46a06b39e378753a2926aeb/tenor.gif',
                                                                'size': 387821
                                                                },
                                                    'loopedmp4': {
                                                                'url': 'https://media.tenor.com/videos/3ef72d6b5e97c18ce1a6303e8bb6ac93/mp4',
                                                                'dims': [200, 266],
                                                                'duration': 3.11304,
                                                                'preview': 'https://media.tenor.com/images/56b7390fdaa0b7a5ce30fadff9ebdbd7/raw'
                                                                }
                                                }
                                    ],
                                        'tags': [],
                                        'shares': 1,
                                        'itemurl': 'https://tenor.com/view/bear-fanny-fart-gif-5364027',
                                        'composite': None,
                                        'hasaudio': False,
                                        'title': '',
                                        'id': '5364027'
                                    }
                                    ],
                    'next': '1'
                    }
