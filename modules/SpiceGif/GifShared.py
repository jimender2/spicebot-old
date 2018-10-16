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
valid_gif_api = ['giphy', 'tenor', 'gfycat']


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
                    "error": None,
                    "gifapi": 'giphy'
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
    page = requests.get(url, headers=None)
    if page.status_code != 200:
        returngifdict["error"] = 'No Results for this search'
        return returngifdict
    data = json.loads(urllib2.urlopen(url).read())
    bot.say("giphy")

    # Verify there are results
    results = data['data']
    resultsarray = []
    for result in results:
        resultsarray.append('https://media2.giphy.com/media/'+result['id']+'/giphy.gif')

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

    if int(searchnum) > int(resultsamount - 1):
        searchnum = randint(0, resultsamount - 1)
    returngifdict["returnnum"] = searchnum

    returngifdict["returnurl"] = resultsarray[searchnum]

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
                    "error": None,
                    "gifapi": 'tenor',
                    "allgifs": []
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

    url = 'https://api.tenor.com/v1/search?q=' + str(searchquery) + '&key=' + str(tenorapi) + '&limit=' + str(searchlimit)
    page = requests.get(url, headers=None)
    if page.status_code != 200:
        returngifdict["error"] = 'No Results for this search'
        return returngifdict
    data = json.loads(urllib2.urlopen(url).read())
    bot.say("tenor")

    # Verify there are results
    results = data['results']
    resultsarray = []
    for result in results:
        cururl = result['url']
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

    if int(searchnum) > int(resultsamount - 1):
        searchnum = randint(0, resultsamount - 1)
    returngifdict["returnnum"] = searchnum

    returngifdict["returnurl"] = resultsarray[searchnum]

    return returngifdict


"""
gfycat
"""


gfycatapi_id = config.get("gfycat", "client_id")
gfycatapi_key = config.get("gfycat", "client_secret")
gfycatlimit = 50


def getGif_gfycat(bot, query, searchnum, searchlimit=gfycatlimit):

    returngifdict = {
                    "query": query,
                    "searchquery": query,
                    "querysuccess": False,
                    "returnnum": searchnum,
                    "returnurl": None,
                    "error": None,
                    "gifapi": 'gfycat',
                    "allgifs": []
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

    url = 'https://api.gfycat.com/v1/gfycats/search?search_text=' + str(searchquery) + '&count=' + str(searchlimit)

    url = str(baseurl + checksite)
    page = requests.get(url, headers=None)
    if page.status_code != 200:
        returngifdict["error"] = 'No Results for this search'
        return returngifdict

    data = json.loads(urllib2.urlopen(url).read())

    # Verify there are results
    results = data['gfycats']
    resultsarray = []
    for result in results:
        cururl = result['gifUrl']
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

    if int(searchnum) > int(resultsamount - 1):
        searchnum = randint(0, resultsamount - 1)
    returngifdict["returnnum"] = searchnum

    returngifdict["returnurl"] = resultsarray[searchnum]

    return returngifdict


"""
All
"""


def getGif_all(bot, query, searchnum, searchlimit=giphylimit):

    gifdict = {
                    "query": query,
                    "searchquery": query,
                    "querysuccess": False,
                    "returnnum": searchnum,
                    "returnurl": None,
                    "error": None,
                    "gifapi": None,
                    "allgifs": []
                    }

    # Make sure there is a valid input of query and search number
    if not query:
        gifdict["error"] = 'No Query to Search'
        return gifdict
    if not str(searchnum).isdigit() and searchnum != 'random':
        gifdict["error"] = 'No Search Number or Random Specified'
        return gifdict

    gifapiresults = []
    for currentapi in valid_gif_api:
        currentgifdict = eval("getGif_" + currentapi + "(bot, query, 'random', searchlimit)")
        if currentgifdict["querysuccess"]:
            gifdictall = currentgifdict["allgifs"]
            gifapiresults.extend(gifdictall)

    if gifapiresults == []:
        gifdict = {
                        "query": query,
                        "searchquery": query,
                        "querysuccess": False,
                        "returnnum": None,
                        "returnurl": None,
                        "error": None,
                        "gifapi": None
                        }
        gifdict["error"] = 'No Results were found for ' + query + ' in any api'
        return gifdict

    random.shuffle(gifapiresults)
    random.shuffle(gifapiresults)
    gifdict = spicemanip(bot, gifapiresults, 'random')
    return gifdict
