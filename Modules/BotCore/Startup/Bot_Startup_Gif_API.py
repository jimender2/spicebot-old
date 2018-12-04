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


"""
This reads the external config for gif api
"""


@event('001')
@rule('.*')
@sopel.module.thread(True)
def bot_startup_gif_api(bot, trigger):

    # don't run jobs if not ready
    while not bot_startup_requirements_met(bot, ["ext_conf"]):
        pass

    bot.memory["botdict"]["tempvals"]['valid_gif_api_dict'] = dict()

    valid_gif_api_dict = {
                            "giphy": {
                                        "url": "http://api.giphy.com/v1/gifs/search?",
                                        "query": 'q=',
                                        "limit": '&limit=',
                                        "id": None,
                                        "api_id": None,
                                        "key": "&api_key=",
                                        "nsfw": None,
                                        "sfw": 'rating=R',
                                        "results": 'data',
                                        "cururl": 'url',
                                        },
                            "tenor": {
                                        "url": "https://api.tenor.com/v1/search?",
                                        "query": 'q=',
                                        "limit": '&limit=',
                                        "id": None,
                                        "api_id": None,
                                        "key": "&key=",
                                        "nsfw": '&contentfilter=off',
                                        "sfw": '&contentfilter=low',
                                        "results": 'results',
                                        "cururl": 'url',
                                        },
                            "gfycat": {
                                        "url": "https://api.gfycat.com/v1/gfycats/search?",
                                        "query": 'search_text=',
                                        "limit": '&count=',
                                        "id": None,
                                        "api_id": None,
                                        "key": None,
                                        "nsfw": '&nsfw=3',
                                        "sfw": '&nsfw=1',
                                        "results": 'gfycats',
                                        "cururl": 'gifUrl',
                                        },
                            "gifme": {
                                        "url": "http://api.gifme.io/v1/search?",
                                        "query": 'query=',
                                        "limit": '&limit=',
                                        "id": None,
                                        "api_id": None,
                                        "key": "&key=",
                                        "nsfw": '&sfw=false',
                                        "sfw": '&sfw=true',
                                        "results": 'data',
                                        "cururl": 'link',
                                        },
                            }

    for gif_api in valid_gif_api_dict.keys():
        if gif_api not in bot.memory["botdict"]["tempvals"]['ext_conf'].keys():
            bot.memory["botdict"]["tempvals"]['ext_conf'][gif_api] = dict()
        if gif_api not in bot.memory["botdict"]["tempvals"]['valid_gif_api_dict'].keys():
            bot.memory["botdict"]["tempvals"]['valid_gif_api_dict'][gif_api] = dict()
        for gif_key_part in valid_gif_api_dict[gif_api].keys():
            if gif_key_part not in bot.memory["botdict"]["tempvals"]['valid_gif_api_dict'][gif_api].keys():
                bot.memory["botdict"]["tempvals"]['valid_gif_api_dict'][gif_api][gif_key_part] = valid_gif_api_dict[gif_api][gif_key_part]

        if "apikey" not in bot.memory["botdict"]["tempvals"]['valid_gif_api_dict'][gif_api].keys():
            if "apikey" in bot.memory["botdict"]["tempvals"]['ext_conf'][gif_api]:
                bot.memory["botdict"]["tempvals"]['valid_gif_api_dict'][gif_api]["apikey"] = bot.memory["botdict"]["tempvals"]['ext_conf'][gif_api]["apikey"]
            else:
                bot.memory["botdict"]["tempvals"]['valid_gif_api_dict'][gif_api]["apikey"] = None

    bot_startup_requirements_set(bot, "gif_api")
