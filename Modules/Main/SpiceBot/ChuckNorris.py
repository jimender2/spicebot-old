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

    jokes = getJoke(bot)

    if botcom.specified:
        if botcom.specified > len(jokes):
            currentspecified = len(jokes)
        else:
            currentspecified = botcom.specified
        botcom.replynum = currentspecified
        botcom.replies = spicemanip(bot, jokes, currentspecified)
    else:
        botcom.replies = spicemanip(bot, jokes, 'random')
        try:
            botcom.replynum = jokes.index(botcom.replies)
        except Exception as e:
            botcom.replynum = 0
        botcom.replynum += 1
    botcom.totalreplies = len(jokes)

    botcom.replies = str("(" + str(botcom.replynum) + "/" + str(botcom.totalreplies)) + ") " + botcom.replies

    if target:
        targetchecking = bot_target_check(bot, botcom, target, ['self'])
        if not targetchecking["targetgood"]:
            return osd(bot, botcom.channel_current, 'say', targetchecking["error"])
    target = nick_actual(bot, target)

    if target:
        for r in (("Chuck Norris's", targetposession(bot, target)), ("Norris's", targetposession(bot, target)), ("Chuck Norris'", targetposession(bot, target)), ("Norris'", targetposession(bot, target)), ('Chuck Norris', target), ('chuck norris', target), ('Norris', target), ('norris', target), ('Chuck', target), ('chuck', target)):
            botcom.replies = botcom.replies.replace(*r)

    osd(bot, trigger.sender, 'say', botcom.replies)


def getJoke(bot):

    url = 'http://api.icndb.com/jokes/'

    jokes = []
    try:
        page = requests.get(url)
        result = page.content
        jsonjokes = json.loads(result)
        jsonjokes = jsonjokes['value']
        for jokenum in jsonjokes:
            # bot.msg("#spicebottest", str(jokenum))
            joke = jokenum['joke']
            joke = joke.replace('&quot;', '\"')
            jokes.append(joke)
    except ValueError:
        jokes = []

    if jokes == []:
        jokes = ["Chuck Norris broke the interwebs."]

    return jokes
