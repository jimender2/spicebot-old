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

# Valid Gif api's
valid_gif_api = ['giphy', 'tenor', 'gfycat', 'gifme']


"""
Giphy
"""


giphyapi = config.get("giphy", "apikey")
giphylimit = 50


def getGif_giphy(bot, searchdict, searchlimit=giphylimit):

    searchdict = gif_searchdict_check(bot, searchdict)

    returngifdict = {
                    "query": searchdict["query"],
                    "searchquery": searchdict["query"],
                    "querysuccess": False,
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
        searchdict["searchnum"] = randint(0, searchlimit)

    url = 'http://api.giphy.com/v1/gifs/search?q=' + str(searchquery) + '&api_key=' + str(giphyapi) + '&limit=' + str(searchlimit)
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
    returngifdict["querysuccess"] = True

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
tenorlimit = 50


def getGif_tenor(bot, searchdict, searchlimit=tenorlimit):

    searchdict = gif_searchdict_check(bot, searchdict)

    returngifdict = {
                    "query": searchdict["query"],
                    "searchquery": searchdict["query"],
                    "querysuccess": False,
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
        searchdict["searchnum"] = randint(0, searchlimit)

    url = 'https://api.tenor.com/v1/search?q=' + str(searchquery) + '&key=' + str(tenorapi) + '&limit=' + str(searchlimit) + '&contentfilter=off'
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
    returngifdict["querysuccess"] = True

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
gfycatlimit = 50


def getGif_gfycat(bot, searchdict, searchlimit=gfycatlimit):

    searchdict = gif_searchdict_check(bot, searchdict)

    returngifdict = {
                    "query": searchdict["query"],
                    "searchquery": searchdict["query"],
                    "querysuccess": False,
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
        searchdict["searchnum"] = randint(0, searchlimit)

    url = 'https://api.gfycat.com/v1/gfycats/search?search_text=' + str(searchquery) + '&count=' + str(searchlimit) + '&nsfw=3'

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
    returngifdict["querysuccess"] = True

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
gifmelimit = 50
gifme_dontusesites = ["http://forgifs.com", "http://a.dilcdn.com", "http://www.bestgifever.com", "http://s3-ec.buzzfed.com", "http://i.minus.com", "http://fap.to", "http://prafulla.net"]


def getGif_gifme(bot, searchdict, searchlimit=gifmelimit):

    searchdict = gif_searchdict_check(bot, searchdict)

    returngifdict = {
                    "query": searchdict["query"],
                    "searchquery": searchdict["query"],
                    "querysuccess": False,
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
        searchdict["searchnum"] = randint(0, searchlimit)

    url = 'http://api.gifme.io/v1/search?query=' + str(searchquery) + '&limit=' + str(searchlimit) + '&nsfw=true&sfw=false' + '&key=' + str(gifmeapi_key)

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
    returngifdict["querysuccess"] = True

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


def getGif_all(bot, searchdict, searchlimit=giphylimit):

    searchdict = gif_searchdict_check(bot, searchdict)

    gifdict = {
                    "query": searchdict["query"],
                    "searchquery": searchdict["query"],
                    "querysuccess": False,
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
    if not str(searchdict["searchnum"]).isdigit() and searchdict["searchnum"] != 'random':
        gifdict["error"] = 'No Search Number or Random Specified'
        return gifdict

    gifapiresults = []
    for currentapi in valid_gif_api:
        currentgifdict = eval("getGif_" + currentapi + "(bot, searchdict, searchlimit)")
        if currentgifdict["querysuccess"]:
            gifdictall = currentgifdict["allgifs"]
            gifapiresults.extend(gifdictall)

    if gifapiresults == []:
        gifdict = {
                        "query": searchdict["query"],
                        "searchquery": searchdict["query"],
                        "querysuccess": False,
                        "returnnum": None,
                        "returnurl": None,
                        "error": None,
                        "gifapi": None
                        }
        gifdict["error"] = 'No Results were found for ' + searchdict["query"] + ' in any api'
        return gifdict

    random.shuffle(gifapiresults)
    random.shuffle(gifapiresults)
    gifdict = spicemanip(bot, gifapiresults, 'random')
    return gifdict


"""
Query Defaults
"""


def gif_searchdict_check(bot, searchdict):
    bot.say(str(searchdict))

    # list of defaults
    query_defaults = {
                    "query": None,
                    "searchnum": 'random'
                    "gifsearch": global valid_gif_api,
                    }

    # set defaults if they don't exist
    for key in query_defaults:
        if key not in searchdict.keys():
            searchdict[key] = query_defaults[key]

    # set api usage
    if not isinstance(searchdict['gifsearch'], list):
        searchdict['gifsearch'] = []
    else:
        for apis in searchdict['gifsearch']:
            if apis not in valid_gif_api:
                searchdict['gifsearch'].remove(apis)

    bot.say(str(searchdict))

    # return search dictionary now that it has been processed
    return searchdict
