#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
sys.path.append(moduledir)
from BotShared import *
import textwrap
import collections
import json
import requests
from sopel.logger import get_logger
from sopel.module import commands, rule, example, priority
sys.setdefaultencoding('utf-8')
import dbbtest_vars


@sopel.module.commands('dbbtest')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    # IF "&&" is in the full input, it is treated as multiple commands, and is split
    commands_array = spicemanip(bot, triggerargsarray, "split_&&")
    if commands_array == []:
        commands_array = [[]]
    for command_split_partial in commands_array:
        triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
        execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    osd(bot, trigger.sender, 'say', "This is deathbybandaid's test module")

    triggerargsarray = spicemanip(bot, trigger.group(2), 'create')

    if 'game_loaded' not in rpg_gamedict.keys():
        bot.say("not loaded")
        rpg_gamedict = get_database_value(bot, 'rpg_game_records', 'rpg_gamedict') or rpg_gamedict
        rpg_gamedict['game_loaded'] = True
    else:
        bot.say("pre loaded")

    bot.say(str(rpg_gamedict))


# Database Users
def get_user_dict(bot, rpg, nick, dictkey):

    # check that db list is there
    if not hasattr(rpg, 'userdb'):
        rpg.userdb = class_create('userdblist')
    if not hasattr(rpg.userdb, 'list'):
        rpg.userdb.list = []

    returnvalue = 0

    # check if nick has been pulled from db already
    if nick not in rpg.userdb.list:
        rpg.userdb.list.append(nick)
        nickdict = get_database_value(bot, nick, rpg.default) or dict()
        createuserdict = str("rpg.userdb." + nick + " = nickdict")
        exec(createuserdict)
    else:
        if not hasattr(rpg.userdb, nick):
            nickdict = dict()
        else:
            nickdict = eval('rpg.userdb.' + nick)

    if dictkey in nickdict.keys():
        returnvalue = nickdict[dictkey]
    else:
        nickdict[dictkey] = 0
        returnvalue = 0

    return returnvalue


# set a value
def set_user_dict(bot, rpg, nick, dictkey, value):
    currentvalue = get_user_dict(bot, rpg, nick, dictkey)
    nickdict = eval('rpg.userdb.' + nick)
    nickdict[dictkey] = value


# reset a value
def reset_user_dict(bot, rpg, nick, dictkey):
    currentvalue = get_user_dict(bot, rpg, nick, dictkey)
    nickdict = eval('rpg.userdb.' + nick)
    if dictkey in nickdict:
        del nickdict[dictkey]


# add or subtract from current value
def adjust_user_dict(bot, rpg, nick, dictkey, value):
    oldvalue = get_user_dict(bot, rpg, nick, dictkey)
    if not str(oldvalue).isdigit():
        oldvalue = 0
    nickdict = eval('rpg.userdb.' + nick)
    nickdict[dictkey] = oldvalue + value


# Save all database users in list
def save_user_dicts(bot, rpg):

    # check that db list is there
    if not hasattr(rpg, 'userdb'):
        rpg.userdb = class_create('userdblist')
    if not hasattr(rpg.userdb, 'list'):
        rpg.userdb.list = []

    for nick in rpg.userdb.list:
        if not hasattr(rpg.userdb, nick):
            nickdict = dict()
        else:
            nickdict = eval('rpg.userdb.' + nick)
        set_database_value(bot, nick, rpg.default, nickdict)


# add or subtract from current value
def adjust_user_dict_array(bot, rpg, nick, dictkey, entries, adjustmentdirection):
    if not isinstance(entries, list):
        entries = [entries]
    oldvalue = get_user_dict(bot, rpg, nick, dictkey)
    nickdict = eval('rpg.userdb.' + nick)
    if not isinstance(oldvalue, list):
        oldvalue = []
    for x in entries:
        if adjustmentdirection == 'add':
            if x not in oldvalue:
                oldvalue.append(x)
        elif adjustmentdirection == 'del':
            if x in oldvalue:
                oldvalue.remove(x)
    nickdict[dictkey] = oldvalue
