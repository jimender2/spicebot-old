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


@sopel.module.commands('youtube', 'yt')
@sopel.module.thread(True)
def mainfunction(bot, trigger):

    botcom = bot_module_prerun(bot, trigger)
    if not botcom.modulerun:
        return

    if not botcom.multiruns:
        execute_main(bot, trigger, botcom)
    else:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip.main(botcom.triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            botcom.triggerargsarray = spicemanip.main(command_split_partial, 'create')
            execute_main(bot, trigger, botcom)

    botdict_save(bot)


def execute_main(bot, trigger, botcom):

    if len(botcom.triggerargsarray) >= 1:
        mysite = spicemanip.main(botcom.triggerargsarray, 1).lower()
        searchterm = spicemanip.main(botcom.triggerargsarray, '1+')
        querystring = spicemanip.main(botcom.triggerargsarray, '2+')
        data = querystring.replace(' ', '+')
        site = '+site%3Ayoutube.com'
        url = 'https://www.youtube.com/'
        url2 = 'https://youtube.com/'
        searchterm = data+site
        query = searchfor(bot, searchterm)
        if not query:
            osd(bot, botcom.channel_current, 'say', 'I cannot find anything about that')
        else:
            if(str(query).startswith(url) or str(query).startswith(url2)):
                osd(bot, botcom.channel_current, 'say', query)
            else:
                osd(bot, botcom.channel_current, 'say', query)
                osd(bot, botcom.channel_current, 'say', 'Valid website not found')

    else:
        osd(bot, botcom.channel_current, 'say', "Enter what you want to search for")


def searchfor(bot, data):
    """Search Google."""
    lookfor = data.replace(':', '%3A')
    try:
        var = requests.get(r'http://www.google.com/search?q=' + lookfor + '&btnI', headers=header)
    except Exception as e:
        var = None

    if var and var.url:
        var = requests.get(r'http://www.google.com/search?q=' + lookfor + '&btnI')
        query = str(var.url)
    else:
        query = None
    return query
