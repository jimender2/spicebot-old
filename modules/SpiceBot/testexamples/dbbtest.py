#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

import textwrap
import collections
import json

import requests

from sopel.logger import get_logger
from sopel.module import commands, rule, example, priority


# @sopel.module.commands('dbbtest')
# def mainfunction(bot, trigger):
#    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
#    execute_main(bot, trigger, triggerargsarray, botcom, instigator)

@sopel.module.commands('dbbtest')
def execute_main(bot, trigger):
    osd(bot, trigger.sender, 'say', "This is deathbybandaid's test module")

    # RPG dynamic Class
    rpg = class_create('main')

    # thisdict = dict(apple="green", banana="yellow", cherry="red")

    # bot.say(str(thisdict["apple"]))

    strength = get_rpg_user_dict(bot, rpg, bot.nick, 'strength')

    bot.say(str(strength))


# Database Users
def get_rpg_user_dict(bot, rpg, nick, value):

    # check that db list is there
    if not hasattr(rpg, 'userdb'):
        rpg.userdb = []

    value = 0

    # check if nick has been pulled from db already
    if nick not in rpg.userdb:
        rpg.userdb.append(nick)
        nickdict = get_database_value(bot, nick, 'rpg') or dict()
        bot.say(str(nickdict))
    # else:
        # nickdict = eval()

    return value
