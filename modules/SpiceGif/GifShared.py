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
from BotShared import *

# author deathbybandaid


# creds
config = ConfigParser.ConfigParser()
config.read("/home/spicebot/spicebot.conf")

dontusesites = [
                        "http://forgifs.com", "http://a.dilcdn.com", "http://www.bestgifever.com",
                        "http://s3-ec.buzzfed.com", "http://i.minus.com", "http://fap.to", "http://prafulla.net",
                        "http://3.bp.blogspot.com"
                        ]


valid_gif_api_dict = {
                        "giphy": {
                                    "url": "http://api.giphy.com/v1/gifs/search?",
                                    "query": 'q=',
                                    "limit": '&limit=',
                                    "key": "&api_key=",
                                    "apikey": config.get("giphy", "apikey"),
                                    "nsfw": None,
                                    "sfw": 'rating=R',
                                    "results": 'data',
                                    "cururl": 'url',
                                    },
                        "tenor": {
                                    "url": "https://api.tenor.com/v1/search?",
                                    "query": 'q=',
                                    "limit": '&limit=',
                                    "key": "&key=",
                                    "apikey": config.get("tenor", "apikey"),
                                    "nsfw": '&contentfilter=off',
                                    "sfw": '&contentfilter=low',
                                    "results": 'results',
                                    "cururl": 'url',
                                    },
                        "gfycat": {
                                    "url": "https://api.gfycat.com/v1/gfycats/search?",
                                    "query": 'search_text=',
                                    "limit": '&count=',
                                    "key": None,
                                    "apikey": None,
                                    "nsfw": '&nsfw=3',
                                    "sfw": '&nsfw=1',
                                    "results": 'gfycats',
                                    "cururl": 'gifUrl',
                                    },
                        "gifme": {
                                    "url": "http://api.gifme.io/v1/search?",
                                    "query": 'query=',
                                    "limit": '&limit=',
                                    "key": "&key=",
                                    "apikey": 'rX7kbMzkGu7WJwvG',
                                    "nsfw": '&sfw=false',
                                    "sfw": '&sfw=true',
                                    "results": 'data',
                                    "cururl": 'link',
                                    },
                        }


def getGif(bot, searchdict):

    # list of defaults
    query_defaults = {
                    "query": None,
                    "searchnum": 'random',
                    "gifsearch": valid_gif_api_dict.keys(),
                    "searchlimit": 'default',
                    "nsfw": False,
                    }

    # set defaults if they don't exist
    for key in query_defaults:
        if key not in searchdict.keys():
            searchdict[key] = query_defaults[key]

    # Replace spaces in search query
    searchdict["searchquery"] = searchdict["query"].replace(' ', '%20')

    # set api usage
    if not isinstance(searchdict['gifsearch'], list):
        if str(searchdict['gifsearch']) in valid_gif_api_dict.keys():
            searchdict['gifsearch'] = [searchdict['gifsearch']]
        else:
            searchdict['gifsearch'] = valid_gif_api_dict.keys()
    else:
        for apis in searchdict['gifsearch']:
            if apis not in valid_gif_api_dict.keys():
                searchdict['gifsearch'].remove(apis)

    # Verify search limit
    if searchdict['searchlimit'] == 'default' or not isinstance(searchdict['searchlimit'], int):
        searchdict['searchlimit'] = 50

    # Random handling for searchnum
    if searchdict["searchnum"] == 'random':
        searchdict["searchnum"] = randint(0, searchdict['searchlimit'])

    # Make sure there is a valid input of query and search number
    if not searchdict["query"]:
        return {"error": 'No Query to Search'}

    if not str(searchdict["searchnum"]).isdigit():
        return {"error": 'No Search Number or Random Specified'}

    gifapiresults = []
    for currentapi in searchdict['gifsearch']:

        # url base
        url = valid_gif_api_dict[currentapi]['url']
        # query
        url += valid_gif_api_dict[currentapi]['query'] + str(searchdict["searchquery"])
        # limit
        url += valid_gif_api_dict[currentapi]['limit'] + str(searchdict["searchlimit"])
        # nsfw search?
        if searchdict['nsfw']:
            url += valid_gif_api_dict[currentapi]['nsfw']
        else:
            url += valid_gif_api_dict[currentapi]['sfw']
        # api key
        url += valid_gif_api_dict[currentapi]['key'] + valid_gif_api_dict[currentapi]['apikey']

        page = requests.get(url, headers=None)
        if page.status_code == 500:
            pass

        data = json.loads(urllib2.urlopen(url).read())

        results = data[valid_gif_api_dict[currentapi]['results']]
        resultsarray = []
        for result in results:
            cururl = result[valid_gif_api_dict[currentapi]['cururl']]
            if str(cururl).endswith(".gif") and not str(cururl).startswith(tuple(dontusesites)):
                resultsarray.append(cururl)

        # make sure there are results
        resultsamount = len(resultsarray)
        if resultsarray == []:
            pass

        # Create Temp dict for every result
        tempresultnum = 0
        for tempresult in resultsarray:
            tempdict = dict()
            tempdict["returnnum"] = tempresultnum
            tempdict["returnurl"] = tempresult
            tempdict["gifapi"] = currentapi
            tempresultnum += 1
            gifapiresults.append(tempdict)

    if gifapiresults == []:
        return {"error": "No Results were found for " + searchdict["query"] + " in the " + str(spicemanip(bot, searchdict['gifsearch'], 'orlist')) + " api(s)"}

    # shuffle and select random entry
    random.shuffle(gifapiresults)
    random.shuffle(gifapiresults)
    gifdict = spicemanip(bot, gifapiresults, 'random')

    # return dict
    gifdict['error'] = None
    return gifdict
