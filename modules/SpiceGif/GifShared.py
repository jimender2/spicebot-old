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


"""
Giphy
"""


giphyapi = config.get("giphy", "apikey")


def getGif_giphy(bot, searchdict):

    returngifdict = {
                    "query": searchdict["query"],
                    "searchquery": searchdict["query"],
                    "returnnum": searchdict["searchnum"],
                    "returnurl": None,
                    "error": None,
                    "gifapi": 'giphy'
                    }

    # Make sure there is a valid input of query and search number
    if not searchdict["query"]:
        returngifdict["error"] = 'No Query to Search'
        return returngifdict
    if not str(searchdict["searchnum"]).isdigit() and searchdict["searchnum"] != 'random':
        returngifdict["error"] = 'No Search Number or Random Specified'
        return returngifdict

    # spaces in query
    searchquery = searchdict["query"].replace(' ', '%20')
    returngifdict["searchquery"] = searchquery

    # Random
    if searchdict["searchnum"] == 'random':
        searchdict["searchnum"] = randint(0, searchdict['searchlimit'])

    url = 'http://api.giphy.com/v1/gifs/search?q=' + str(searchquery) + '&api_key=' + str(giphyapi) + '&limit=' + str(searchdict['searchlimit'])
    page = requests.get(url, headers=None)
    if page.status_code == 500:
        returngifdict["error"] = 'No Results for this search'
        return returngifdict
    data = json.loads(urllib2.urlopen(url).read())

    # Verify there are results
    results = data['data']
    resultsarray = []
    for result in results:
        cururl = 'https://media2.giphy.com/media/'+result['id']+'/giphy.gif'
        if str(cururl).endswith(".gif"):
            resultsarray.append(cururl)

    resultsamount = len(resultsarray)
    if resultsarray == []:
        returngifdict["error"] = 'No Giphy Results were found for ' + returngifdict['query']
        return returngifdict

    allresults = []
    tempresultnum = 0
    for tempresult in resultsarray:
        tempdict = returngifdict.copy()
        tempdict["returnnum"] = tempresultnum
        tempdict["returnurl"] = tempresult
        tempresultnum += 1
        allresults.append(tempdict)
    returngifdict["allgifs"] = allresults

    if int(searchdict["searchnum"]) > int(resultsamount - 1):
        searchdict["searchnum"] = randint(0, resultsamount - 1)
    returngifdict["returnnum"] = searchdict["searchnum"]

    returngifdict["returnurl"] = resultsarray[searchdict["searchnum"]]

    return returngifdict


"""
Tenor
"""

tenorapi = config.get("tenor", "apikey")


def getGif_tenor(bot, searchdict):

    returngifdict = {
                    "query": searchdict["query"],
                    "searchquery": searchdict["query"],
                    "returnnum": searchdict["searchnum"],
                    "returnurl": None,
                    "error": None,
                    "gifapi": 'tenor',
                    "allgifs": []
                    }

    # Make sure there is a valid input of query and search number
    if not searchdict["query"]:
        returngifdict["error"] = 'No Query to Search'
        return returngifdict
    if not str(searchdict["searchnum"]).isdigit() and searchdict["searchnum"] != 'random':
        returngifdict["error"] = 'No Search Number or Random Specified'
        return returngifdict

    # spaces in query
    searchquery = searchdict["query"].replace(' ', '%20')
    returngifdict["searchquery"] = searchquery

    # Random
    if searchdict["searchnum"] == 'random':
        searchdict["searchnum"] = randint(0, searchdict['searchlimit'])

    url = 'https://api.tenor.com/v1/search?q=' + str(searchquery) + '&key=' + str(tenorapi) + '&limit=' + str(searchdict['searchlimit'])  # + '&contentfilter=off'
    page = requests.get(url, headers=None)
    if page.status_code == 500:
        returngifdict["error"] = 'No Results for this search'
        return returngifdict
    data = json.loads(urllib2.urlopen(url).read())

    # Verify there are results
    results = data['results']
    resultsarray = []
    for result in results:
        cururl = result['url']
        if str(cururl).endswith(".gif"):
            resultsarray.append(cururl)

    resultsamount = len(resultsarray)
    if resultsarray == []:
        returngifdict["error"] = 'No Tenor Results were found for ' + returngifdict['query']
        return returngifdict

    allresults = []
    tempresultnum = 0
    for tempresult in resultsarray:
        tempdict = returngifdict.copy()
        tempdict["returnnum"] = tempresultnum
        tempdict["returnurl"] = tempresult
        tempresultnum += 1
        allresults.append(tempdict)
    returngifdict["allgifs"] = allresults

    if int(searchdict["searchnum"]) > int(resultsamount - 1):
        searchdict["searchnum"] = randint(0, resultsamount - 1)
    returngifdict["returnnum"] = searchdict["searchnum"]

    returngifdict["returnurl"] = resultsarray[searchdict["searchnum"]]

    return returngifdict


"""
gfycat
"""


gfycatapi_id = config.get("gfycat", "client_id")
gfycatapi_key = config.get("gfycat", "client_secret")


def getGif_gfycat(bot, searchdict):

    returngifdict = {
                    "query": searchdict["query"],
                    "searchquery": searchdict["query"],
                    "returnnum": searchdict["searchnum"],
                    "returnurl": None,
                    "error": None,
                    "gifapi": 'gfycat',
                    "allgifs": []
                    }

    # Make sure there is a valid input of query and search number
    if not searchdict["query"]:
        returngifdict["error"] = 'No Query to Search'
        return returngifdict
    if not str(searchdict["searchnum"]).isdigit() and searchdict["searchnum"] != 'random':
        returngifdict["error"] = 'No Search Number or Random Specified'
        return returngifdict

    # spaces in query
    searchquery = searchdict["query"].replace(' ', '%20')
    returngifdict["searchquery"] = searchquery

    # Random
    if searchdict["searchnum"] == 'random':
        searchdict["searchnum"] = randint(0, searchdict['searchlimit'])

    url = 'https://api.gfycat.com/v1/gfycats/search?search_text=' + str(searchquery) + '&count=' + str(searchdict['searchlimit']) + '&nsfw=3'

    page = requests.get(url, headers=None)
    if page.status_code == 500:
        returngifdict["error"] = 'No Results for this search'
        return returngifdict

    data = json.loads(urllib2.urlopen(url).read())

    # Verify there are results
    results = data['gfycats']
    resultsarray = []
    for result in results:
        cururl = result['gifUrl']
        if str(cururl).endswith(".gif"):
            resultsarray.append(cururl)

    resultsamount = len(resultsarray)
    if resultsarray == []:
        returngifdict["error"] = 'No Gfycat Results were found for ' + returngifdict['query']
        return returngifdict

    allresults = []
    tempresultnum = 0
    for tempresult in resultsarray:
        tempdict = returngifdict.copy()
        tempdict["returnnum"] = tempresultnum
        tempdict["returnurl"] = tempresult
        tempresultnum += 1
        allresults.append(tempdict)
    returngifdict["allgifs"] = allresults

    if int(searchdict["searchnum"]) > int(resultsamount - 1):
        searchdict["searchnum"] = randint(0, resultsamount - 1)
    returngifdict["returnnum"] = searchdict["searchnum"]

    returngifdict["returnurl"] = resultsarray[searchdict["searchnum"]]

    return returngifdict


"""
gifme.io
"""


gifmeapi_key = 'rX7kbMzkGu7WJwvG'
gifme_dontusesites = [
                        "http://forgifs.com", "http://a.dilcdn.com", "http://www.bestgifever.com",
                        "http://s3-ec.buzzfed.com", "http://i.minus.com", "http://fap.to", "http://prafulla.net",
                        "http://3.bp.blogspot.com"
                        ]


def getGif_gifme(bot, searchdict):

    returngifdict = {
                    "query": searchdict["query"],
                    "searchquery": searchdict["query"],
                    "returnnum": searchdict["searchnum"],
                    "returnurl": None,
                    "error": None,
                    "gifapi": 'gifme',
                    "allgifs": []
                    }

    # Make sure there is a valid input of query and search number
    if not searchdict["query"]:
        returngifdict["error"] = 'No Query to Search'
        return returngifdict
    if not str(searchdict["searchnum"]).isdigit() and searchdict["searchnum"] != 'random':
        returngifdict["error"] = 'No Search Number or Random Specified'
        return returngifdict

    # spaces in query
    searchquery = searchdict["query"].replace(' ', '%20')
    returngifdict["searchquery"] = searchquery

    # Random
    if searchdict["searchnum"] == 'random':
        searchdict["searchnum"] = randint(0, searchdict['searchlimit'])

    url = 'http://api.gifme.io/v1/search?query=' + str(searchquery) + '&limit=' + str(searchdict['searchlimit']) + '&nsfw=true&sfw=false' + '&key=' + str(gifmeapi_key)

    page = requests.get(url, headers=None)
    if page.status_code == 500:
        returngifdict["error"] = 'No Results for this search'
        return returngifdict

    data = json.loads(urllib2.urlopen(url).read())

    # Verify there are results
    results = data['data']
    resultsarray = []
    for result in results:
        cururl = result['link']
        if not str(cururl).startswith(tuple(gifme_dontusesites)):
            if str(cururl).endswith(".gif"):
                resultsarray.append(cururl)

    resultsamount = len(resultsarray)
    if resultsarray == []:
        returngifdict["error"] = 'No Gifme Results were found for ' + returngifdict['query']
        return returngifdict

    allresults = []
    tempresultnum = 0
    for tempresult in resultsarray:
        tempdict = returngifdict.copy()
        tempdict["returnnum"] = tempresultnum
        tempdict["returnurl"] = tempresult
        tempresultnum += 1
        allresults.append(tempdict)
    returngifdict["allgifs"] = allresults

    if int(searchdict["searchnum"]) > int(resultsamount - 1):
        searchdict["searchnum"] = randint(0, resultsamount - 1)
    returngifdict["returnnum"] = searchdict["searchnum"]

    returngifdict["returnurl"] = resultsarray[searchdict["searchnum"]]

    return returngifdict


"""
All
"""


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

    gifdict = {
                    "query": searchdict["query"],
                    "searchquery": searchdict["searchquery"],
                    "returnnum": searchdict["query"],
                    "returnurl": None,
                    "error": None,
                    "gifapi": None,
                    "allgifs": []
                    }

    # Make sure there is a valid input of query and search number
    if not searchdict["query"]:
        gifdict["error"] = 'No Query to Search'
        return gifdict

    if not str(searchdict["searchnum"]).isdigit():
        gifdict["error"] = 'No Search Number or Random Specified'
        return gifdict

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
            if str(cururl).endswith(".gif"):  # and not str(cururl).startswith(tuple(dontusesites)):
                resultsarray.append(cururl)

        # make sure there are results
        resultsamount = len(resultsarray)
        if resultsarray == []:
            pass
        bot.say(str(resultsarray))

        # Create Temp dict for every result
        tempresultnum = 0
        for tempresult in resultsarray:
            bot.say(str(tempresult))
            tempdict = dict()
            tempdict["returnnum"] = tempresultnum
            tempdict["returnurl"] = tempresult
            tempdict["gifapi"] = currentapi
            tempresultnum += 1
            gifapiresults.append(tempdict)

    if gifapiresults == []:
        gifdict["error"] = "No Results were found for " + searchdict["query"] + " in the " + str(spicemanip(bot, searchdict['gifsearch'], 'orlist')) + " api(s)"
        return gifdict

    # shuffle and select random entry
    random.shuffle(gifapiresults)
    random.shuffle(gifapiresults)
    gifdict = spicemanip(bot, gifapiresults, 'random')

    # return dict
    return gifdict
