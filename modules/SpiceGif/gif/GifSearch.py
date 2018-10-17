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
gifshareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(gifshareddir)
from BotShared import *
from GifShared import *

# author deathbybandaid


@sopel.module.commands('gifadmin')
def gifadmin(bot, trigger):

    if not trigger.admin and not bot.privileges[trigger.sender.lower()][trigger.nick.lower()] >= module.OP:
        return osd(bot, trigger.sender, 'say',  "Only Admins and OPs may adjust the gif settings.")


@sopel.module.commands('gif', 'tenor', 'giphy', 'gfycat', 'gifme')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        botcom.commandused = trigger.group(1)
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):

    if botcom.commandused == 'gif':
        searchapis = valid_gif_api_dict.keys()
    else:
        searchapis = [botcom.commandused]

    searchdict = {"query": query, "gifsearch": searchapis}

    nsfwenabled = get_database_value(bot, bot.nick, 'channels_nsfw') or []
    if botcom.channel_current in nsfwenabled:
        searchdict['nsfw'] = True

    query = spicemanip(bot, triggerargsarray, 0)
    gifdict = getGif(bot, searchdict)

    if gifdict["error"]:
        osd(bot, trigger.sender, 'say',  str(gifdict["error"]))
        return

    osd(bot, trigger.sender, 'say',  gifdict['gifapi'].title() + " Result (" + str(query) + " #" + str(gifdict["returnnum"]) + "): " + str(gifdict["returnurl"]))
