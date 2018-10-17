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

# contributers jimender2

quickgifdict = {
                "template": {
                    "query": "test",  # optional, if not there, query defaults to the key used
                    "searchapis": ['giphy', 'tenor'],  # optional, if you want to specify apis used
                    "searchfail": ["test failed"],  # optional, if you want a special message due to failure, list form will select randomly
                    "saytype": 'say',  # optional, if this is an action or say
                    },
                "template_altcom": {"altcom": "alt_template"},  # alternate command functionality

                "borg": {
                    "query": "Jeri Ryan",
                    "searchfail": ["Resistance is futile"],
                    },

                "boobies": {
                    "query": "boobies",
                    "searchfail": ["https://giphy.com/gifs/26FLf3L9bDpYCVO5G/html5"],
                    },

                "bs": {
                    "query": "bullshit",
                    "searchfail": ["https://media.giphy.com/media/iqGVHdU2tEBq9JSrtm/giphy.gif"],
                    },

                "darwin": {
                    "query": "Darwin Award",
                    "searchfail": ["is not a contender for the Darwin award, thank fuck."],
                    "saytype": 'action',
                    },

                "facepalm": {
                    "searchfail": ["There is not enough facepalm in the world for this"],
                    },

                "ibb": {
                    "query": "I'll be back",
                    "searchfail": ["https://tenor.com/view/arnold-schwarzenegger-the-terminator-ill-be-back-gif-4367793"],
                    },
                "illbeback": {"altcom": "ibb"},

                "tmyk": {
                    "query": "the more you know",
                    "searchfail": ['the more you know... **magic fingers**'],
                    "saytype": 'action',
                    },
                "themoreyouknow": {"altcom": "tmyk"}, "myk": {"altcom": "tmyk"}, "moreyouknow": {"altcom": "tmyk"},

                "nike": {
                    "query": "Just do it",
                    "searchfail": ['thinks you should stop being a little bitch and just do it.'],
                    "saytype": 'action',
                    },

                "smh": {
                    "searchfail": ['shakes his head...'],
                    "saytype": 'action',
                    },
                }


@sopel.module.commands('borg', 'boobies', 'bs', 'darwin', 'facepalm', 'ibb', 'illbeback', 'tmyk', 'themoreyouknow', 'myk', 'moreyouknow', 'nike', 'smh')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        botcom.commandused = trigger.group(1)
        if "altcom" in quickgifdict[botcom.commandused].keys():
            botcom.commandused = quickgifdict[botcom.commandused]["altcom"]
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):

    if "query" not in quickgifdict[botcom.commandused].keys():
        query = str(botcom.commandused)
    else:
        query = quickgifdict[botcom.commandused]["query"]

    searchdict = {"query": query}

    if "searchapis" in quickgifdict[botcom.commandused].keys():
        searchdict['gifsearch'] = quickgifdict[botcom.commandused]["searchapis"]

    nsfwenabled = get_database_value(bot, bot.nick, 'channels_nsfw') or []
    if botcom.channel_current in nsfwenabled:
        searchdict['nsfw'] = True

    gifdict = getGif(bot, searchdict)
    if gifdict["error"]:

        if "searchfail" in quickgifdict[botcom.commandused].keys():
            saytype = 'say'
            if "saytype" not in quickgifdict[botcom.commandused].keys():
                saytype = quickgifdict[botcom.commandused]
            faillist = quickgifdict[botcom.commandused]["searchfail"]
            if not isinstance(faillist, list):
                faillist = [str(faillist)]
            return osd(bot, trigger.sender, saytype, spicemanip(bot, faillist, 'random'))
        else:
            return osd(bot, trigger.sender, 'say',  str(gifdict["error"]))

    osd(bot, trigger.sender, 'say',  gifdict['gifapi'].title() + " Result (" + str(query) + " #" + str(gifdict["returnnum"]) + "): " + str(gifdict["returnurl"]))
