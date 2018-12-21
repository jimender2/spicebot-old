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

comdict = {
            "author": "deathbybandaid",
            "contributors": [],
            "description": "",
            'privs': [],
            "example": "",
            "exampleresponse": "",
            }


@sopel.module.commands('chucknorris', 'chuck')
def mainfunction(bot, trigger):

    botcom = bot_module_prerun(bot, trigger)
    if not botcom.modulerun:
        return

    if not botcom.multiruns:
        execute_main(bot, trigger, botcom)
    else:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, botcom.triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            botcom.triggerargsarray = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, botcom)

    botdict_save(bot)


def execute_main(bot, trigger, botcom):

    target = spicemanip(bot, botcom.triggerargsarray, 1) or None

    joke = getJoke()

    if target:
        targetchecking = bot_target_check(bot, botcom, target, [])
        if not targetchecking["targetgood"]:
            return osd(bot, botcom.channel_current, 'say', targetchecking["error"])
    target = nick_actual(bot, target)

    if target:
        for r in (("Chuck Norris'", targetposession(bot, target)), ("Norris'", targetposession(bot, target)), ('Chuck Norris', target), ('chuck norris', target), ('Norris', target), ('norris', target), ('Chuck', target), ('chuck', target)):
            joke = joke.replace(*r)

    osd(bot, trigger.sender, 'say', joke)


def getJoke():

    url = 'http://api.icndb.com/jokes/random'

    try:
        page = requests.get(url)
        result = page.content
        jsonjoke = json.loads(result)
        joke = jsonjoke['value']['joke']
        joke = joke.replace('&quot;', '\"')

    except ValueError:
        joke = "Chuck Norris broke the interwebs."

    return joke
