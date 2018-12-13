#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
from sopel import module, tools
import sopel.module
from sopel.module import commands, nickname_commands, event, rule, OP, ADMIN, VOICE, HALFOP, OWNER, thread, priority, example, NOLIMIT
from sopel.tools import Identifier, stderr, SopelMemory, iterkeys
from sopel.tools.time import get_timezone, format_time
from sopel.formatting import *


# imports for system and OS access, directories
import os
from os.path import exists
import sys

# additional shared files
moduledir = os.path.dirname(__file__)
sys.path.append(moduledir)

# API
import socket
import threading
import subprocess
from threading import Thread
import netifaces

# Additional imports
import feedparser
import ConfigParser
import copy
import datetime
import time
import re
import random
import arrow
import fnmatch
import urllib
import git
import requests
from lxml import html
from time import strptime
from dateutil import parser
import calendar
import arrow
import pytz
from dateutil import tz
from xml.dom import minidom
import json
import xmltodict
from fake_useragent import UserAgent
import praw
from prawcore import NotFound
import twitter
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client.file import Storage
import httplib2
from word2number import w2n
import codecs
import urllib2
from BeautifulSoup import BeautifulSoup
from random import randint, randrange
import collections
from num2words import num2words
from difflib import SequenceMatcher
from more_itertools import sort_together
from operator import itemgetter
from statistics import mean
import itertools
import inspect
import pickle
from bson import json_util
import textwrap
import httplib
import speedtest

from sopel.logger import get_logger
LOGGER = get_logger(__name__)


# user agent and header
ua = UserAgent()
header = {'User-Agent': str(ua.chrome)}


# Ensure Encoding
reload(sys)
sys.setdefaultencoding('utf-8')


"""
Dictionaries
"""


hardcode_dict = {
                "bot_ip_addresses": ["192.168.5.100", "192.168.5.101"],
                }


os_dict = {
            "user": "spicebot",
            "ext_conf": "spicebot.conf",
            }


bot_dict = {

            "tempvals": {},

            }


api_dict = {
            "addresses": [],
            }


github_dict = {
                "url_main": "https://github.com/",
                "url_api": "https://api.github.com/repos/",
                "url_raw": "https://raw.githubusercontent.com/",
                "url_path_wiki": "/wiki",
                "url_path_issues": "/issues",
                "repo_owner": "SpiceBot",
                "repo_name": "SpiceBot",
                }


mode_dict_alias = {
                    "+o": "OP", "-o": "deOP",
                    "+v": "VOICE", "-v": "deVOICE",
                    "+h": "HOP", "-h": "deHOP",
                    "+a": "ADMIN", "-a": "deADMIN",
                    "+q": "OWNER", "-q": "deOWNER",
                    "+b": "BAN", "-b": "unBAN",
                    "+c": "noCOLOR", "-c": "COLOR",
                    #  TODO add more user/channel modes
                    }


gif_dontusesites = [
                        "http://forgifs.com", "http://a.dilcdn.com", "http://www.bestgifever.com",
                        "http://s3-ec.buzzfed.com", "http://i.minus.com", "http://fap.to", "http://prafulla.net",
                        "http://3.bp.blogspot.com"
                        ]

gif_dontuseextensions = ['.jpg', '.png']


valid_com_types = ['simple', 'fillintheblank', 'targetplusreason', 'sayings', "readfromfile", "readfromurl", "ascii_art", "gif", "translate", "responses", "feeds"]


# valid commands that the bot will reply to by name
valid_botnick_commands = {
                            "github": {
                                        'privs': [],
                                        },
                            "docs": {
                                        'privs': [],
                                        },
                            "wiki": {
                                        'privs': [],
                                        },
                            "help": {
                                        'privs': [],
                                        },
                            "uptime": {
                                        'privs': [],
                                        },
                            "canyouseeme": {
                                        'privs': [],
                                        },
                            "gender": {
                                        'privs': [],
                                        },
                            "owner": {
                                        'privs': [],
                                        },
                            "admins": {
                                        'privs': [],
                                        },
                            "channel": {
                                        'privs': [],
                                        },
                            "msg": {
                                    'privs': ['admin', 'OP'],
                                    },
                            "action": {
                                        'privs': ['admin', 'OP'],
                                        },
                            "notice": {
                                        'privs': ['admin', 'OP'],
                                        },
                            "debug": {
                                        'privs': ['admin', 'OP'],
                                        },
                            "logs": {
                                        'privs': ['admin', 'OP'],
                                        },
                            "update": {
                                        'privs': ['admin', 'OP'],
                                        },
                            "restart": {
                                        'privs': ['admin', 'OP'],
                                        },
                            "permfix": {
                                        'privs': ['admin', 'OP'],
                                        },
                            "pip": {
                                        'privs': ['admin', 'OP'],
                                        },
                            "cd": {
                                        'privs': ['admin', 'OP'],
                                        },
                            "dir": {
                                        'privs': ['admin', 'OP'],
                                        },
                            "gitpull": {
                                        'privs': ['admin', 'OP'],
                                        },
                            "auth": {
                                        'privs': ['admin', 'OP'],
                                        },
                            "sweep": {
                                        'privs': ['admin', 'OP'],
                                        },
                            }


"""
Botdict
"""


# open dictionary, and import saved values from database
def botdict_setup_open(bot):

    # if existing in memory, save, and then close and reopen
    if "botdict" in bot.memory:
        botdict_save(bot)
        del bot.memory["botdict"]

    # open global dict
    global bot_dict
    botdict = bot_dict

    # pull from database and merge, some content is static
    opendict = botdict.copy()
    dbbotdict = get_database_value(bot, bot.nick, 'bot_dict') or dict()
    opendict = merge_botdict(opendict, dbbotdict)
    botdict.update(opendict)

    # done loading
    bot.memory["botdict"] = botdict


# Merge database dict with stock
def merge_botdict(a, b, path=None):
    "merges b into a"
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge_botdict(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                a[key] = b[key]
        else:
            a[key] = b[key]
    return a


# This is how the dict is saved to the database
def botdict_save(bot):
    savedict = copy.deepcopy(bot.memory["botdict"])

    # Values to not save to database
    savedict_del = ['tempvals', 'static']
    for dontsave in savedict_del:
        if dontsave in savedict.keys():
            del savedict[dontsave]

    # save to database
    set_database_value(bot, bot.nick, 'bot_dict', savedict)


"""
Botdict
"""


def botcom_nick(bot, trigger):

    # don't run jobs if not ready
    while not bot_startup_requirements_met(bot, ["botdict", "monologue"]):
        pass

    # botcom dynamic Class
    botcom = class_create('botcom')
    botcom.default = 'botcom'

    # what time was this triggered
    botcom.timestart = time.time()

    # instigator
    botcom.instigator = str(trigger.nick)
    botcom.instigator_hostmask = str(trigger.hostmask)
    botcom.instigator_user = str(trigger.user)

    # bot credentials
    botcom.admin = trigger.admin
    botcom.owner = trigger.owner

    # server
    botcom.server = bot.memory["botdict"]["tempvals"]['server']

    # channel
    botcom.channel_current = str(trigger.sender).lower()
    botcom.channel_priv = trigger.is_privmsg

    # create arg list
    botcom.triggerargsarray = spicemanip(bot, trigger, '2+', 'list')

    botcom.command_main = spicemanip(bot, botcom.triggerargsarray, 1)

    return botcom


def botcom_symbol_trigger(bot, trigger):

    # don't run jobs if not ready
    while not bot_startup_requirements_met(bot, ["botdict", "monologue"]):
        pass

    # botcom dynamic Class
    botcom = class_create('botcom')
    botcom.default = 'botcom'

    # what time was this triggered
    botcom.timestart = time.time()

    # instigator
    botcom.instigator = str(trigger.nick)
    botcom.instigator_hostmask = str(trigger.hostmask)
    botcom.instigator_user = str(trigger.user)

    # bot credentials
    botcom.admin = trigger.admin
    botcom.owner = trigger.owner

    # server
    botcom.server = bot.memory["botdict"]["tempvals"]['server']

    # channel
    botcom.channel_current = str(trigger.sender).lower()
    botcom.channel_priv = trigger.is_privmsg

    # create arg list
    botcom.triggerargsarray = spicemanip(bot, trigger, 'create')

    return botcom


"""
Core Bot Permissions
"""


def bot_nickcom_run_check(bot, botcom):

    commandrun = True

    if 'privs' in valid_botnick_commands[botcom.command_main.lower()].keys():
        commandrunconsensus = []

        if 'admin' in valid_botnick_commands[botcom.command_main.lower()]['privs']:
            if botcom.instigator not in bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]['bot_admins']:
                commandrunconsensus.append('False')
            else:
                commandrunconsensus.append('True')

        if 'OP' in valid_botnick_commands[botcom.command_main.lower()]['privs']:
            if not botcom.channel_priv:
                if botcom.instigator not in bot.memory["botdict"]["tempvals"]['servers_list'][botcom.server]['channels_list'][botcom.channel_current]['chanops']:
                    commandrunconsensus.append('False')
                else:
                    commandrunconsensus.append('True')
            else:
                commandrunconsensus.append('False')

        if 'HOP' in valid_botnick_commands[botcom.command_main.lower()]['privs']:
            if not botcom.channel_priv:
                if botcom.instigator not in bot.memory["botdict"]["tempvals"]['servers_list'][botcom.server]['channels_list'][botcom.channel_current]['chanhalfops']:
                    commandrunconsensus.append('False')
                else:
                    commandrunconsensus.append('True')
            else:
                commandrunconsensus.append('False')

        if 'VOICE' in valid_botnick_commands[botcom.command_main.lower()]['privs']:
            if not botcom.channel_priv:
                if botcom.instigator not in bot.memory["botdict"]["tempvals"]['servers_list'][botcom.server]['channels_list'][botcom.channel_current]['chanvoices']:
                    commandrunconsensus.append('False')
                else:
                    commandrunconsensus.append('True')
            else:
                commandrunconsensus.append('False')

        if 'OWNER' in valid_botnick_commands[botcom.command_main.lower()]['privs']:
            if not botcom.channel_priv:
                if botcom.instigator not in bot.memory["botdict"]["tempvals"]['servers_list'][botcom.server]['channels_list'][botcom.channel_current]['chanowners']:
                    commandrunconsensus.append('False')
                else:
                    commandrunconsensus.append('True')
            else:
                commandrunconsensus.append('False')

        if 'ADMIN' in valid_botnick_commands[botcom.command_main.lower()]['privs']:
            if not botcom.channel_priv:
                if botcom.instigator not in bot.memory["botdict"]["tempvals"]['servers_list'][botcom.server]['channels_list'][botcom.channel_current]['chanadmins']:
                    commandrunconsensus.append('False')
                else:
                    commandrunconsensus.append('True')
            else:
                commandrunconsensus.append('False')

        if valid_botnick_commands[botcom.command_main.lower()]['privs'] == []:
            commandrunconsensus.append('True')

        if 'True' not in commandrunconsensus:
            commandrun = False

    return commandrun


def bot_command_run_check(bot, botcom, privsrequired):

    commandrun = True

    commandrunconsensus = []

    if 'admin' in privsrequired:
        if botcom.instigator not in bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]['bot_admins']:
            commandrunconsensus.append('False')
        else:
            commandrunconsensus.append('True')

    if 'OP' in privsrequired:
        if not botcom.channel_priv:
            if botcom.instigator not in bot.memory["botdict"]["tempvals"]['servers_list'][botcom.server]['channels_list'][botcom.channel_current]['chanops']:
                commandrunconsensus.append('False')
            else:
                commandrunconsensus.append('True')
        else:
            commandrunconsensus.append('False')

    if 'HOP' in privsrequired:
        if not botcom.channel_priv:
            if botcom.instigator not in bot.memory["botdict"]["tempvals"]['servers_list'][botcom.server]['channels_list'][botcom.channel_current]['chanhalfops']:
                commandrunconsensus.append('False')
            else:
                commandrunconsensus.append('True')
        else:
            commandrunconsensus.append('False')

    if 'VOICE' in privsrequired:
        if not botcom.channel_priv:
            if botcom.instigator not in bot.memory["botdict"]["tempvals"]['servers_list'][botcom.server]['channels_list'][botcom.channel_current]['chanvoices']:
                commandrunconsensus.append('False')
            else:
                commandrunconsensus.append('True')
        else:
            commandrunconsensus.append('False')

    if 'OWNER' in privsrequired:
        if not botcom.channel_priv:
            if botcom.instigator not in bot.memory["botdict"]["tempvals"]['servers_list'][botcom.server]['channels_list'][botcom.channel_current]['chanowners']:
                commandrunconsensus.append('False')
            else:
                commandrunconsensus.append('True')
        else:
            commandrunconsensus.append('False')

    if 'ADMIN' in privsrequired:
        if not botcom.channel_priv:
            if botcom.instigator not in bot.memory["botdict"]["tempvals"]['servers_list'][botcom.server]['channels_list'][botcom.channel_current]['chanadmins']:
                commandrunconsensus.append('False')
            else:
                commandrunconsensus.append('True')
        else:
            commandrunconsensus.append('False')

    if privsrequired == []:
        commandrunconsensus.append('True')

    if 'True' not in commandrunconsensus:
        commandrun = False

    return commandrun


"""
Module Prerun
"""


def bot_module_prerun(bot, trigger, bypasscom=None):

    # don't run jobs if not ready
    while not bot_startup_requirements_met(bot, ["botdict", "monologue"]):
        pass

    # botcom dynamic Class
    botcom = class_create('botcom')
    botcom.default = 'botcom'

    # what time was this triggered
    botcom.timestart = time.time()

    # default if module will run
    botcom.modulerun = True

    # instigator
    botcom.instigator = str(trigger.nick)
    botcom.instigator_hostmask = str(trigger.hostmask)
    botcom.instigator_user = str(trigger.user)

    # bot credentials
    botcom.admin = trigger.admin
    botcom.owner = trigger.owner

    # server
    botcom.server = bot.memory["botdict"]["tempvals"]['server']

    # channel
    botcom.channel_current = str(trigger.sender).lower()
    botcom.channel_priv = trigger.is_privmsg

    # Bots can't run commands
    if bot_check_inlist(bot, botcom.instigator, str(bot.nick)):
        botcom.modulerun = False
        return botcom

    # create arg list
    botcom.triggerargsarray = spicemanip(bot, trigger, 'create')

    # the command that was run
    if not bypasscom:
        botcom.maincom = spicemanip(bot, botcom.triggerargsarray, 1).lower()[1:]
        botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+', "list")
    else:
        botcom.maincom = bypasscom.lower()

    # command aliases
    if botcom.maincom in bot.memory["botdict"]["tempvals"]['module_commands'].keys():
        if "aliasfor" in bot.memory["botdict"]["tempvals"]['module_commands'][botcom.maincom].keys():
            botcom.maincom = bot.memory["botdict"]["tempvals"]['module_commands'][botcom.maincom]["aliasfor"]

    # allow && splitting
    botcom.multiruns = True
    if botcom.maincom in bot.memory["botdict"]['servers_list'][botcom.server]['channels_list'][str(botcom.channel_current)]["multirun_disabled_commands"].keys():
        botcom.multiruns = False

    botcom.dotcommand_dict = copy.deepcopy(bot.memory["botdict"]["tempvals"]['module_commands'][botcom.maincom])

    # This allows users to specify which reply by number by using an ! and a digit (first or last in string)
    validspecifides = ['block', 'unblock', 'last', 'random', 'count', 'view', 'add', 'del', 'remove', 'special', 'contribs', 'contrib', "contributors", 'author', "alias", "filepath", "enable", "disable", "multiruns"]
    botcom.specified = None
    argone = spicemanip(bot, botcom.triggerargsarray, 1)
    if str(argone).startswith("--") and len(str(argone)) > 2:
        if str(argone[2:]).isdigit():
            botcom.specified = int(argone[2:])
        elif bot_check_inlist(bot, str(argone[2:]), validspecifides):
            botcom.specified = str(argone[2:]).lower()
        else:
            try:
                botcom.specified = w2n.word_to_num(str(argone[1:]))
            except ValueError:
                botcom.specified = None
        if botcom.specified:
            botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+', 'list')

    # Hardcoded commands Below
    if botcom.specified == 'enable':
        botcom.modulerun = False

        if botcom.channel_priv:
            osd(bot, botcom.instigator, 'notice', "This command must be run in the channel you which to " + botcom.specified + " it in.")
            return botcom

        if botcom.maincom not in bot.memory["botdict"]['servers_list'][botcom.server]['channels_list'][str(botcom.channel_current)]["disabled_commands"].keys():
            osd(bot, botcom.channel_current, 'say', botcom.maincom + " is already " + botcom.specified + "d in " + str(botcom.channel_current))
            return botcom

        if not bot_command_modding_auth(bot, botcom):
            osd(bot, botcom.channel_current, 'say', "You are not authorized to " + botcom.specified + " " + botcom.maincom + " in " + str(botcom.channel_current))
            return botcom

        del bot.memory["botdict"]['servers_list'][botcom.server]['channels_list'][str(botcom.channel_current)]["disabled_commands"][botcom.maincom]
        osd(bot, botcom.channel_current, 'say', botcom.maincom + " is now " + botcom.specified + "d in " + str(botcom.channel_current))
        botdict_save(bot)
        return botcom

    elif botcom.specified == 'disable':
        botcom.modulerun = False

        if botcom.channel_priv:
            osd(bot, botcom.instigator, 'notice', "This command must be run in the channel you which to " + botcom.specified + " it in.")
            return botcom

        if botcom.maincom in bot.memory["botdict"]['servers_list'][botcom.server]['channels_list'][str(botcom.channel_current)]["disabled_commands"].keys():
            osd(bot, botcom.channel_current, 'say', botcom.maincom + " is already " + botcom.specified + "d in " + str(botcom.channel_current))
            return botcom

        if not bot_command_modding_auth(bot, botcom):
            osd(bot, botcom.channel_current, 'say', "You are not authorized to " + botcom.specified + " " + botcom.maincom + " in " + str(botcom.channel_current))
            return botcom

        trailingmessage = spicemanip(bot, botcom.triggerargsarray, 0) or "No reason given."
        timestamp = str(datetime.datetime.utcnow())
        bot.memory["botdict"]['servers_list'][botcom.server]['channels_list'][str(botcom.channel_current)]["disabled_commands"][botcom.maincom] = {"reason": trailingmessage, "timestamp": timestamp, "disabledby": botcom.instigator}
        osd(bot, botcom.channel_current, 'say', botcom.maincom + " is now " + botcom.specified + "d in " + str(botcom.channel_current) + " at " + str(timestamp) + " for the following reason: " + trailingmessage)
        botdict_save(bot)
        return botcom

    elif botcom.specified == 'multiruns':
        botcom.modulerun = False

        if botcom.channel_priv:
            osd(bot, botcom.instigator, 'notice', "This argument must be run in channel.")
            return botcom

        if not bot_command_modding_auth(bot, botcom):
            osd(bot, botcom.channel_current, 'say', "You are not authorized to turn " + botcom.specified + " multicom usage in " + str(botcom.channel_current))
            return botcom

        onoff = spicemanip(bot, botcom.triggerargsarray, 1)
        if onoff == 'on':
            if botcom.maincom not in bot.memory["botdict"]['servers_list'][botcom.server]['channels_list'][str(botcom.channel_current)]["multirun_disabled_commands"].keys():
                osd(bot, botcom.channel_current, 'say', botcom.maincom + " already has multicom usage " + onoff + " in " + str(botcom.channel_current))
            else:
                del bot.memory["botdict"]['servers_list'][botcom.server]['channels_list'][str(botcom.channel_current)]["multirun_disabled_commands"][botcom.maincom]
                osd(bot, botcom.channel_current, 'say', botcom.maincom + " now has multicom usage " + onoff + " in " + str(botcom.channel_current))
        elif onoff == 'off':
            if botcom.maincom in bot.memory["botdict"]['servers_list'][botcom.server]['channels_list'][str(botcom.channel_current)]["multirun_disabled_commands"].keys():
                osd(bot, botcom.channel_current, 'say', botcom.maincom + " already has multicom usage " + onoff + " in " + str(botcom.channel_current))
            else:
                trailingmessage = spicemanip(bot, botcom.triggerargsarray, "2+") or "No reason given."
                timestamp = str(datetime.datetime.utcnow())
                bot.memory["botdict"]['servers_list'][botcom.server]['channels_list'][str(botcom.channel_current)]["multirun_disabled_commands"][botcom.maincom] = {"reason": trailingmessage, "timestamp": timestamp, "multi_disabledby": botcom.instigator}
                osd(bot, botcom.channel_current, 'say', botcom.maincom + " now has multicom usage " + onoff + " in " + str(botcom.channel_current))
        else:
            if botcom.maincom not in bot.memory["botdict"]['servers_list'][botcom.server]['channels_list'][str(botcom.channel_current)]["multirun_disabled_commands"].keys():
                osd(bot, botcom.channel_current, 'say', botcom.maincom + " allows multicom use in " + str(botcom.channel_current))
            else:
                osd(bot, botcom.channel_current, 'say', botcom.maincom + " does not allow multicom use in " + str(botcom.channel_current))
        botdict_save(bot)
        return botcom

    elif botcom.specified == 'block':
        botcom.modulerun = False

        if not bot_command_modding_auth(bot, botcom):
            osd(bot, botcom.channel_current, 'say', "You are not authorized to enable/disable command usage.")
            return botcom

        posstarget = spicemanip(bot, botcom.triggerargsarray, 1) or 0
        if not posstarget:
            osd(bot, botcom.channel_current, 'say', "Who am I blocking from " + str(botcom.maincom) + " usage?")
            return botcom

        if posstarget not in bot.memory["botdict"]["users"].keys():
            osd(bot, botcom.channel_current, 'say', "I don't know who " + str(posstarget) + " is.")
            return botcom

        currentblocks = get_nick_value(bot, posstarget, "long", 'commands', "unallowed") or []
        if botcom.maincom in currentblocks:
            osd(bot, botcom.channel_current, 'say', str(posstarget) + " is already blocked from using " + botcom.maincom + ".")
            return botcom

        adjust_nick_array(bot, posstarget, "long", 'commands', "unallowed", [botcom.maincom], 'add')
        botdict_save(bot)

        osd(bot, botcom.channel_current, 'say', str(posstarget) + " has been blocked from using " + botcom.maincom + ".")
        return botcom

    elif botcom.specified == 'unblock':
        botcom.modulerun = False

        if not bot_command_modding_auth(bot, botcom):
            osd(bot, botcom.channel_current, 'say', "You are not authorized to enable/disable command usage.")
            return botcom

        posstarget = spicemanip(bot, botcom.triggerargsarray, 1) or 0
        if not posstarget:
            osd(bot, botcom.channel_current, 'say', "Who am I unblocking from " + str(botcom.maincom) + " usage?")
            return botcom

        if posstarget not in bot.memory["botdict"]["users"].keys():
            osd(bot, botcom.channel_current, 'say', "I don't know who " + str(posstarget) + " is.")
            return botcom

        currentblocks = get_nick_value(bot, posstarget, "long", 'commands', "unallowed") or []
        if botcom.maincom not in currentblocks:
            osd(bot, botcom.channel_current, 'say', str(posstarget) + " is already not blocked from using " + botcom.maincom + ".")
            return botcom

        adjust_nick_array(bot, posstarget, "long", 'commands', "unallowed", [botcom.maincom], 'del')
        botdict_save(bot)

        osd(bot, botcom.channel_current, 'say', str(posstarget) + " has been unblocked from using " + botcom.maincom + ".")
        return botcom

    elif botcom.specified == 'special':
        botcom.modulerun = False

        osd(bot, botcom.channel_current, 'say', "The " + botcom.specified + " argument is not available for module commands.")
        return botcom

    elif botcom.specified == 'count':
        botcom.modulerun = False

        osd(bot, botcom.channel_current, 'say', "The " + botcom.specified + " argument is not available for module commands.")
        return botcom

    elif botcom.specified == 'filepath':
        botcom.modulerun = False

        osd(bot, botcom.channel_current, 'say', "The " + str(botcom.maincom) + " file is located at " + str(botcom.dotcommand_dict["filepath"]))
        return botcom

    elif botcom.specified == 'author':
        botcom.modulerun = False

        osd(bot, botcom.channel_current, 'say', "The author of the " + str(botcom.maincom) + " command is " + botcom.dotcommand_dict["author"] + ".")
        return botcom

    elif botcom.specified in ['contribs', 'contrib', "contributors"]:
        botcom.modulerun = False

        osd(bot, botcom.channel_current, 'say', "The contributors of the " + str(botcom.maincom) + " command are " + spicemanip(bot, botcom.dotcommand_dict["contributors"], "andlist") + ".")
        return botcom

    elif botcom.specified == 'alias':
        botcom.modulerun = False

        osd(bot, botcom.channel_current, 'say', "The alaises of the " + str(botcom.maincom) + " command are " + spicemanip(bot, botcom.dotcommand_dict["validcoms"], "andlist") + ".")
        return botcom

    elif botcom.specified == 'view':
        botcom.modulerun = False

        osd(bot, botcom.channel_current, 'say', "The " + botcom.specified + " argument is not available for module commands.")
        return botcom

    elif botcom.specified == 'add':
        botcom.modulerun = False

        osd(bot, botcom.channel_current, 'say', "The " + botcom.specified + " argument is not available for module commands.")
        return botcom

    elif botcom.specified in ['del', 'remove']:
        botcom.modulerun = False

        osd(bot, botcom.channel_current, 'say', "The " + botcom.specified + " argument is not available for module commands.")
        return botcom

    currentblocks = get_nick_value(bot, botcom.instigator, "long", 'commands', "unallowed") or []
    if botcom.maincom in currentblocks:
        botcom.modulerun = False
        osd(bot, botcom.channel_current, 'say', "You appear to have been blocked by a bot admin from using the " + botcom.maincom + " command.")
        return botcom

    if not botcom.channel_priv:

        if botcom.maincom in bot.memory["botdict"]['servers_list'][botcom.server]['channels_list'][str(botcom.channel_current)]["disabled_commands"].keys():
            botcom.modulerun = False
            reason = bot.memory["botdict"]['servers_list'][botcom.server]['channels_list'][str(botcom.channel_current)]["disabled_commands"][str(botcom.maincom)]["reason"]
            timestamp = bot.memory["botdict"]['servers_list'][botcom.server]['channels_list'][str(botcom.channel_current)]["disabled_commands"][str(botcom.maincom)]["timestamp"]
            bywhom = bot.memory["botdict"]['servers_list'][botcom.server]['channels_list'][str(botcom.channel_current)]["disabled_commands"][str(botcom.maincom)]["disabledby"]
            osd(bot, botcom.channel_current, 'say', "The " + str(botcom.maincom) + " command was disabled by " + bywhom + " in " + str(botcom.channel_current) + " at " + str(timestamp) + " for the following reason: " + str(reason))
            return botcom

    return botcom


def bot_command_modding_auth(bot, botcom):
    commandrunconsensus, commandrun = [], True
    if botcom.instigator not in bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]['bot_admins']:
        commandrunconsensus.append('False')
    else:
        commandrunconsensus.append('True')
    if botcom.instigator not in bot.memory["botdict"]["tempvals"]['servers_list'][botcom.server]['channels_list'][botcom.channel_current]['chanops']:
        commandrunconsensus.append('False')
    else:
        commandrunconsensus.append('True')
    if botcom.instigator not in bot.memory["botdict"]["tempvals"]['servers_list'][botcom.server]['channels_list'][botcom.channel_current]['chanowners']:
        commandrunconsensus.append('False')
    else:
        commandrunconsensus.append('True')
    if botcom.instigator not in bot.memory["botdict"]["tempvals"]['servers_list'][botcom.server]['channels_list'][botcom.channel_current]['chanadmins']:
        commandrunconsensus.append('False')
    else:
        commandrunconsensus.append('True')
    if 'True' not in commandrunconsensus:
        return False
    else:
        return True


"""
Startup Requirements
"""


def bot_startup_requirements_met(bot, listreq):

    if not isinstance(listreq, list):
        listreq = [str(listreq)]

    if "bot_startup" not in bot.memory:
        bot.memory["bot_startup"] = dict()

    continueconsensus = []

    for requirement in listreq:
        if requirement in bot.memory["bot_startup"].keys():
            continueconsensus.append("True")
        else:
            continueconsensus.append("False")

    if "False" in continueconsensus:
        return False
    else:
        return True


def bot_startup_requirements_set(bot, addonreq):

    if "bot_startup" not in bot.memory:
        bot.memory["bot_startup"] = dict()

    bot.memory["bot_startup"][str(addonreq)] = True


"""
API
"""


def bot_api_port_test(bot, host, port):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((str(host), int(port)))
    if result == 0:
        return True
    else:
        return False


def bot_api_fetch_tcp(bot, TCP_PORT, TCP_IP):
    botdict_return = None

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))

    s.send("GET")

    data = ''
    while True:
        part = s.recv(4096)
        data += part
        if len(part) == 0:
            break
    s.close()

    datasplit = data.splitlines()
    for line in datasplit:
        if len(line) > 100:
            data = line

    try:
        botdict_return = json.loads(data, object_hook=json_util.object_hook)
    except Exception as e:
        return None

    return botdict_return


def bot_api_fetch_web(bot, botport, host):
    botdict_return = None

    # what url to check
    addr = str("http://" + str(host) + ":" + str(botport))

    # try to get data
    try:
        page = requests.get(addr)
    except Exception as e:
        return botdict_return

    # examine results
    result = page.content
    botdict_return = json.loads(result, object_hook=json_util.object_hook)

    return botdict_return


def bot_api_send(bot, botport, messagedict, host):

    # Create a TCP/IP socket
    tempsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = (str(host), int(botport))
    tempsock.connect(server_address)

    # convert to json
    msg = json.dumps(messagedict, default=json_util.default).encode('utf-8')

    # sending all this stuff
    try:
        bot_logging(bot, "API", "[API] Sending data.")
        tempsock.send(msg.encode(encoding="utf-8"))
    except Exception as e:
        bot_logging(bot, "API", "[API] Error Sending Data: (%s)" % (e))

    tempsock.close()

    return


def bot_api_response_headers(bot, msg):
    # response_headers
    response_headers = {
                        'Content-Type': 'text/html; encoding=utf8',
                        'Content-Length': len(msg),
                        'Connection': 'close',
                        }
    response_headers_raw = ''.join('%s: %s\r\n' % (k, v) for k, v in response_headers.items())
    r = '%s %s %s\r\n' % ('HTTP/1.1', '200', 'OK')
    return response_headers_raw, r


def bot_api_send_all(bot, nick, processtype, longevity, sortingkey, usekey, value, timestamp):

    databasedict = {
                    "processtype": processtype,
                    "longevity": longevity,
                    "sortingkey": sortingkey,
                    "usekey": usekey,
                    "value": value,
                    "nick": nick,
                    "type": "databaseentry",
                    }

    hostslist = hardcode_dict["bot_ip_addresses"]
    hostsprocess = []
    for host in hostslist:
        for i in range(8000, 8051):

            # don't process current bot
            if host in bot.memory["botdict"]["tempvals"]['networking']['ip_addresses'] and str(i) == str(bot.memory['sock_port']):
                donothing = True
            else:

                if bot_api_port_test(bot, host, i):
                    hostdict = {"host": host, "port": i}
                    hostsprocess.append(hostdict)

    # this is where we will process the info from the other bots
    for hostdict in hostsprocess:
        try:
            bot_api_send(bot, botport, databasedict, host)
        except Exception as e:
            apiquery = dict()


def bot_api_send_self_command(bot, botcom, commandsent):

    if commandsent not in ["update", "restart"]:
        return

    if 'sock_port' not in bot.memory:
        return
    if not bot.memory['sock_port']:
        return
    portnum = int(bot.memory['sock_port'])

    databasedict = {"type": "command", "command": commandsent, "sender": str(botcom.instigator)}
    bot_api_send(bot, portnum, databasedict, 'localhost')


"""
Feeds
"""


def bot_dictcom_feeds_handler(bot, feed, forcedisplay):

    feed_dict = bot.memory["botdict"]["tempvals"]['feeds'][feed]

    dispmsg = []
    displayname = False

    url = feed_dict["url"]
    if not url:
        if forcedisplay:
            return ["URL missing."]
        else:
            return []

    page = requests.get(url, headers=header)

    if page.status_code == 200:

        now = datetime.datetime.utcnow()
        now = now.replace(tzinfo=pytz.UTC)

        feed_type = feed_dict["type"]

        if feed_type in ['rss', 'youtube', 'github', 'redditrss']:

            try:
                feedjson = feedparser.parse(url)
            except Exception as e:
                if forcedisplay:
                    return ["No Content Usable."]
                else:
                    return []

            lastbuildtime = get_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildtime') or datetime.datetime(1999, 1, 1, 1, 1, 1, 1).replace(tzinfo=pytz.UTC)
            lastbuildtime = parser.parse(str(lastbuildtime))
            try:
                entrytime = feedjson.entries[0].updated
            except Exception as e:
                entrytime = datetime.datetime(1999, 1, 1, 1, 1, 1, 1).replace(tzinfo=pytz.UTC)
            entrytime = parser.parse(str(entrytime))

            lastbuildtitle = get_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildtitle') or None
            try:
                title = feedjson.entries[0].title
                title = unicode_string_cleanup(title)
            except Exception as e:
                title = None
            if title:
                dispmsg.append(title)

            lastbuildlink = get_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildlink') or None
            try:
                link = feedjson.entries[0].link
            except Exception as e:
                link = None
            if link:
                dispmsg.append(link)

            if (entrytime > lastbuildtime and link != lastbuildlink and title != lastbuildtitle) or forcedisplay:
                displayname = feed_dict["displayname"]
                if not displayname:
                    try:
                        displayname = feedjson['feed']['title']
                    except Exception as e:
                        displayname = None
            else:
                dispmsg = []

            if not forcedisplay:
                set_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildtime', str(entrytime))
                set_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildtitle', str(lastbuildtitle))
                set_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildlink', str(lastbuildlink))

        elif feed_type == 'redditapi':

            if not bot.memory["botdict"]["tempvals"]['reddit']:
                if forcedisplay:
                    return ["reddit api unavailable."]
                else:
                    return []

            path = feed_dict["path"]
            if not path:
                if forcedisplay:
                    return ["reddit Path missing."]
                else:
                    return []

            currentsubreddit = feed_dict["path"]

            subredditcheck = reddit_subreddit_check(bot, currentsubreddit)
            if not subredditcheck["exists"]:
                if forcedisplay:
                    return [subredditcheck["error"]]
                else:
                    return []

            try:
                subreddit = bot.memory["botdict"]["tempvals"]['reddit'].subreddit(currentsubreddit)
            except Exception as e:
                if forcedisplay:
                    return ["No Content Usable."]
                else:
                    return []

            try:
                submissions = subreddit.new(limit=1)
                listarray = []
                for submission in submissions:
                    listarray.append(submission)
                submission = listarray[0]
            except Exception as e:
                if forcedisplay:
                    return ["No Content Usable."]
                else:
                    return []

            lastbuildtime = get_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildtime') or datetime.datetime(1999, 1, 1, 1, 1, 1, 1).replace(tzinfo=pytz.UTC)
            lastbuildtime = parser.parse(str(lastbuildtime))
            try:
                entrytime = submission.created
                entrytime = datetime.datetime.fromtimestamp(entrytime).replace(tzinfo=pytz.UTC)
            except Exception as e:
                entrytime = datetime.datetime(1999, 1, 1, 1, 1, 1, 1).replace(tzinfo=pytz.UTC)
            entrytime = parser.parse(str(entrytime))

            try:
                submissionscore = str(submission.score)
            except Exception as e:
                submissionscore = None
            if submissionscore:
                dispmsg.append("{" + str(submissionscore) + "}")

            try:
                nsfw = subreddit.over18
            except Exception as e:
                nsfw = False
            if nsfw:
                dispmsg.append("<NSFW>")

            lastbuildtitle = get_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildtitle') or None
            try:
                title = submission.title
                title = unicode_string_cleanup(title)
            except Exception as e:
                title = None
            if title:
                dispmsg.append(title)

            lastbuildlink = get_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildlink') or None
            try:
                link = submission.permalink
            except Exception as e:
                link = None
            if link:
                dispmsg.append(str(feed_dict["url"] + link))

            if (entrytime > lastbuildtime and link != lastbuildlink and title != lastbuildtitle) or forcedisplay:
                displayname = feed_dict["displayname"]
                if not displayname:
                    displayname = None
            else:
                dispmsg = []

            if not forcedisplay:
                set_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildtime', str(entrytime))
                set_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildtitle', str(lastbuildtitle))
                set_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildlink', str(lastbuildlink))

        elif feed_type == 'twitter':

            if not bot.memory["botdict"]["tempvals"]['twitter']:
                if forcedisplay:
                    return ["twitter api unavailable."]
                else:
                    return []

            handle = feed_dict["handle"]
            if not handle:
                if forcedisplay:
                    return ["twitter handle missing."]
                else:
                    return []

            currenttweetat = feed_dict["handle"]

            try:
                submissions = bot.memory["botdict"]["tempvals"]['twitter'].GetUserTimeline(screen_name=currenttweetat, count=1, exclude_replies=True, include_rts=False)
                submission = submissions[0]
            except Exception as e:
                if forcedisplay:
                    return ["No Content Usable."]
                else:
                    return []

            lastbuildtime = get_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildtime') or datetime.datetime(1999, 1, 1, 1, 1, 1, 1).replace(tzinfo=pytz.UTC)
            lastbuildtime = parser.parse(str(lastbuildtime))
            try:
                entrytime = submission.created_at
                entrytime = entrytime.replace(tzinfo=pytz.UTC)
            except Exception as e:
                entrytime = datetime.datetime(1999, 1, 1, 1, 1, 1, 1).replace(tzinfo=pytz.UTC)
            entrytime = parser.parse(str(entrytime))

            lastbuildtitle = get_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildtitle') or None
            try:
                title = submission.text
                title = unicode_string_cleanup(title)
            except Exception as e:
                title = None
            if title:
                dispmsg.append(title)

            lastbuildlink = get_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildlink') or None
            try:
                link = str(currenttweetat + "/status/" + str(submission.id))
            except Exception as e:
                link = None
            if link:
                dispmsg.append(str(feed_dict["url"] + "/" + link))

            if (entrytime > lastbuildtime and link != lastbuildlink and title != lastbuildtitle) or forcedisplay:
                displayname = feed_dict["displayname"]
                if not displayname:
                    displayname = None
            else:
                dispmsg = []

            if not forcedisplay:
                set_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildtime', str(entrytime))
                set_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildtitle', str(lastbuildtitle))
                set_nick_value(bot, str(bot.nick), 'long', 'feeds', feed + '_lastbuildlink', str(lastbuildlink))

        elif feed_type == 'googlecalendar':

            if not bot.memory["botdict"]["tempvals"]['google']:
                if forcedisplay:
                    return ["google api unavailable."]
                else:
                    return []

            calendar = feed_dict["calendar"]
            if not calendar:
                if forcedisplay:
                    return ["google calendar missing."]
                else:
                    return []

            currentcalendar = feed_dict["calendar"]

            http_auth = bot.memory["botdict"]["tempvals"]['google'].authorize(httplib2.Http())
            service = build('calendar', 'v3', http=http_auth, cache_discovery=False)

            events_result = service.events().list(timeZone='UTC', calendarId=currentcalendar, maxResults=1, singleEvents=True, orderBy='startTime', timeMin=str(str(now.year) + "-" + str(now.month) + "-" + str(now.day) + "T" + str(now.hour) + ":" + str(now.minute) + ":00.000Z")).execute()
            events = events_result.get('items', [])
            if events == []:
                if forcedisplay:
                    return ["No upcoming events on this calendar"]
                else:
                    return []
            nextevent = events[0]

            try:
                entrytime = nextevent["start"]["dateTime"]
            except Exception as e:
                if forcedisplay:
                    return ["Timestamp Error"]
                else:
                    return []
            entrytime = parser.parse(str(entrytime)).replace(tzinfo=pytz.UTC)

            timeuntil = (entrytime - now).total_seconds()
            if timeuntil > 0:
                timecompare = humanized_time((entrytime - now).total_seconds())
                timecompare = str(timecompare + " from now")
            else:
                timecompare = humanized_time((now - entrytime).total_seconds())
                timecompare = str(timecompare + " ago")
            # timecompare = arrow_time(now, entrytime)
            dispmsg.append(timecompare)

            try:
                title = nextevent["summary"]
                title = unicode_string_cleanup(title)
            except Exception as e:
                title = None
            if title:
                dispmsg.append(title)

            if not feed_dict["link"]:
                try:
                    link = str(nextevent["location"])
                    url = findurlsinstring(link)
                    if url != []:
                        link = url[0]
                    else:
                        link = None
                except Exception as e:
                    link = None
                if not link:
                    try:
                        link = str(nextevent["description"])
                        url = findurlsinstring(link)
                        if url != []:
                            link = url[0]
                        else:
                            link = None
                    except Exception as e:
                        link = None
                if not link:
                    try:
                        link = str(nextevent["htmlLink"])
                    except Exception as e:
                        link = None
            else:
                link = feed_dict["link"]
            if link:
                dispmsg.append(link)

            if (int(timeuntil) < 900 and int(timeuntil) > 840) or forcedisplay:

                displayname = feed_dict["displayname"]
                if not displayname:
                    displayname = None
            else:
                dispmsg = []

        elif feed_type == 'webinarscrapes':

            tree = html.fromstring(page.content)

            scrapetime = feed_dict["scrapetime"]
            scrapetimezone = feed_dict["scrapetimezone"]

            try:
                entrytime = tree.xpath(scrapetime)
                if isinstance(entrytime, list):
                    entrytime = entrytime[0]
                entrytime = str(entrytime)
                for r in (("['", ""), ("']", ""), ("\\n", ""), ("\\t", ""), ("@ ", "")):
                    entrytime = entrytime.replace(*r)
                entrytime = parser.parse(entrytime)
                if not tz_aware(entrytime):
                    feedtimezone = pytz.timezone(feed_dict["scrapetimezone"])
                    entrytime = feedtimezone.localize(entrytime)
            except Exception as e:
                if forcedisplay:
                    return ["Timestamp Error"]
                else:
                    return []

            timeuntil = (entrytime - now).total_seconds()
            if timeuntil > 0:
                timecompare = humanized_time((entrytime - now).total_seconds())
                timecompare = str(timecompare + " from now")
            else:
                timecompare = humanized_time((now - entrytime).total_seconds())
                timecompare = str(timecompare + " ago")
            # timecompare = arrow_time(now, entrytime)
            dispmsg.append(timecompare)

            scrapetitle = feed_dict["scrapetitle"]
            if scrapetitle:
                try:
                    title = tree.xpath(scrapetitle)
                    if isinstance(title, list):
                        title = title[0]
                    title = str(title)
                    for r in (("u'", ""), ("['", ""), ("[", ""), ("']", ""), ("\\n", ""), ("\\t", "")):
                        title = title.replace(*r)
                    title = unicode_string_cleanup(title)
                except Exception as e:
                    title = None
                if title:
                    dispmsg.append(title)

            scrapelink = feed_dict["scrapelink"]
            if scrapelink:
                try:
                    link = tree.xpath(scrapelink)
                    if isinstance(link, list):
                        link = link[0]
                    link = str(link)
                    for r in (("['", ""), ("']", "")):
                        link = link.replace(*r)
                    if feed_dict["linkprecede"]:
                        link = str(feed_dict["linkprecede"] + link)
                except Exception as e:
                    link = None
                if link:
                    dispmsg.append(link)

            scrapebonus = feed_dict["scrapebonus"]
            if scrapebonus:
                try:
                    bonus = tree.xpath(scrapebonus)
                    if isinstance(bonus, list):
                        bonus = bonus[0]
                    bonus = str(bonus)
                    scrapebonussplit = feed_dict["scrapebonussplit"]
                    if scrapebonussplit:
                        bonus = str(bonus.split(feed_dict["scrapebonussplit"])[-1])
                    for r in (("\\r", ""), ("\\n", ""), ("']", ""), ("]", ""), ('"', ''), (" '", ""), ("['", ""), ("[", "")):
                        bonus = bonus.replace(*r)
                    bonus = unicode_string_cleanup(bonus)
                except Exception as e:
                    bonus = None
                if bonus:
                    dispmsg.append(bonus)

            if (int(timeuntil) < 900 and int(timeuntil) > 840) or forcedisplay:

                displayname = feed_dict["displayname"]
                if not displayname:
                    displayname = None
            else:
                dispmsg = []

        elif feed_type == 'dailyscrapes':
            if not forcedisplay:
                return []

            tree = html.fromstring(page.content)

            todaytime = datetime.datetime(now.year, now.month, now.day, int(feed_dict["scrapehour"]), int(feed_dict["scrapeminute"]), 0, 0).replace(tzinfo=None)
            entrytime = str(entrytime)
            entrytime = parser.parse(entrytime)
            feedtimezone = pytz.timezone(feed_dict["scrapetimezone"])
            entrytime = feedtimezone.localize(entrytime)

            timeuntil = (entrytime - now).total_seconds()
            if timeuntil < 0:

                tomorrow = now + datetime.timedelta(days=1)
                entrytime = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, int(feed_dict["scrapehour"]), int(feed_dict["scrapeminute"]), 0, 0).replace(tzinfo=None)
                entrytime = str(entrytime)
                entrytime = parser.parse(entrytime)
                feedtimezone = pytz.timezone(feed_dict["scrapetimezone"])
                entrytime = feedtimezone.localize(entrytime)

            bot.msg("#spicebottest", str(entrytime))

            return dispmsg

            scrapetime = feed_dict["scrapetime"]
            scrapetimezone = feed_dict["scrapetimezone"]

            try:
                entrytime = tree.xpath(scrapetime)
                if isinstance(entrytime, list):
                    entrytime = entrytime[0]
                entrytime = str(entrytime)
                for r in (("['", ""), ("']", ""), ("\\n", ""), ("\\t", ""), ("@ ", "")):
                    entrytime = entrytime.replace(*r)
                entrytime = parser.parse(entrytime)
                if not tz_aware(entrytime):
                    feedtimezone = pytz.timezone(feed_dict["scrapetimezone"])
                    entrytime = feedtimezone.localize(entrytime)
            except Exception as e:
                if forcedisplay:
                    return ["Timestamp Error"]
                else:
                    return []

            timeuntil = (entrytime - now).total_seconds()
            if timeuntil > 0:
                timecompare = humanized_time((entrytime - now).total_seconds())
                timecompare = str(timecompare + " from now")
            else:
                timecompare = humanized_time((now - entrytime).total_seconds())
                timecompare = str(timecompare + " ago")
            # timecompare = arrow_time(now, entrytime)
            dispmsg.append(timecompare)

            scrapetitle = feed_dict["scrapetitle"]
            if scrapetitle:
                try:
                    title = tree.xpath(scrapetitle)
                    if isinstance(title, list):
                        title = title[0]
                    title = str(title)
                    for r in (("u'", ""), ("['", ""), ("[", ""), ("']", ""), ("\\n", ""), ("\\t", "")):
                        title = title.replace(*r)
                    title = unicode_string_cleanup(title)
                except Exception as e:
                    title = None
                if title:
                    dispmsg.append(title)

            scrapelink = feed_dict["scrapelink"]
            if scrapelink:
                try:
                    link = tree.xpath(scrapelink)
                    if isinstance(link, list):
                        link = link[0]
                    link = str(link)
                    for r in (("['", ""), ("']", "")):
                        link = link.replace(*r)
                    if feed_dict["linkprecede"]:
                        link = str(feed_dict["linkprecede"] + link)
                except Exception as e:
                    link = None
                if link:
                    dispmsg.append(link)

            scrapebonus = feed_dict["scrapebonus"]
            if scrapebonus:
                try:
                    bonus = tree.xpath(scrapebonus)
                    if isinstance(bonus, list):
                        bonus = bonus[0]
                    bonus = str(bonus)
                    scrapebonussplit = feed_dict["scrapebonussplit"]
                    if scrapebonussplit:
                        bonus = str(bonus.split(feed_dict["scrapebonussplit"])[-1])
                    for r in (("\\r", ""), ("\\n", ""), ("']", ""), ("]", ""), ('"', ''), (" '", ""), ("['", ""), ("[", "")):
                        bonus = bonus.replace(*r)
                    bonus = unicode_string_cleanup(bonus)
                except Exception as e:
                    bonus = None
                if bonus:
                    dispmsg.append(bonus)

            if (int(timeuntil) < 900 and int(timeuntil) > 840) or forcedisplay:

                displayname = feed_dict["displayname"]
                if not displayname:
                    displayname = None
            else:
                dispmsg = []

    if displayname and feed_dict["displayname"]:
        dispmsg.insert(0, "[" + displayname + "]")

    botdict_save(bot)
    return dispmsg


def findurlsinstring(string):
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
    return url


def hashave(mylist):
    if len(mylist) > 1:
        hashave = 'have'
    else:
        hashave = 'has'
    return hashave


def tz_aware(dt):
    if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
        return False
    elif dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None:
        return True


"""
Reddit
"""


def reddit_subreddit_check(bot, sub):
    returndict = {"exists": True, "error": None}
    try:
        bot.memory["botdict"]["tempvals"]['reddit'].subreddits.search_by_name(sub, exact=True)
    except NotFound:
        returndict["error"] = str(sub + " appears to not exist!")
        returndict["exists"] = False
        return returndict

    try:
        subtype = bot.memory["botdict"]["tempvals"]['reddit'].subreddit(sub).subreddit_type
    except Exception as e:
        returndict["exists"] = False
        if str(e) == "received 403 HTTP response":
            returndict["error"] = str(sub + " appears to be an private subreddit!")
            return returndict
        elif str(e) == "received 404 HTTP response":
            returndict["error"] = str(sub + " appears to be an banned subreddit!")
            return returndict
        else:
            returndict["error"] = str(sub + " appears to not have a type")
            return returndict

    return returndict


def reddit_user_exists(bot, user):
    returndict = {"exists": True, "error": None}
    try:
        bot.memory["botdict"]["tempvals"]['reddit'].redditor(user).fullname
    except NotFound:
        returndict["exists"] = False
        returndict["error"] = str(user + " appears to not exist!")
        return returndict
    return returndict


"""
Bot Temp Logging
"""


def bot_logging(bot, logtype, logentry):

    if 'logs' not in bot.memory:
        bot.memory['logs'] = {}

    if logtype not in bot.memory['logs'].keys():
        bot.memory['logs'][logtype] = []

    bot.memory['logs'][logtype].append(logentry)
    if len(bot.memory['logs'][logtype]) > 10:
        del bot.memory['logs'][logtype][0]


"""
Target Checking
"""


def bot_check_inlist(bot, searchterm, searchlist):

    # verify we are searching a list
    if not isinstance(searchlist, list):
        searchlist = [searchlist]
    rebuildlist = []
    for searchitem in searchlist:
        rebuildlist.append(str(searchitem))

    searchterm = str(searchterm)

    if searchterm in rebuildlist:
        return True
    elif searchterm.lower() in [searching.lower() for searching in rebuildlist]:
        return True
    else:
        return False


def nick_actual(bot, nick, altlist=None):
    nick_actual = nick
    if "botdict_loaded" not in bot.memory:
        for u in bot.users:
            if u.lower() == str(nick).lower():
                nick_actual = u
        return nick_actual
    if not altlist:
        searchuserlist = bot.memory["botdict"]["users"].keys()
    else:
        searchuserlist = altlist
    for u in searchuserlist:
        if u.lower() == str(nick).lower():
            nick_actual = u
    return nick_actual


def bot_random_valid_target(bot, botcom, outputtype):
    validtargs = []
    if botcom.channel_priv:
        validtargs.extend([str(bot.nick), botcom.instigator])
    else:
        for user in bot.memory["botdict"]["tempvals"]['servers_list'][botcom.server]['channels_list'][botcom.channel_current]['current_users']:
            targetchecking = bot_target_check(bot, botcom, user, [])
            if targetchecking["targetgood"]:
                validtargs.append(user)
    if outputtype == 'list':
        return validtargs
    elif outputtype == 'random':
        return spicemanip(bot, validtargs, 'random')


def bot_target_check(bot, botcom, target, targetbypass):
    targetgood = {"targetgood": True, "error": "None", "reason": None}

    if not isinstance(targetbypass, list):
        targetbypass = [targetbypass]

    if "notarget" not in targetbypass:
        if not target or target == '':
            return {"targetgood": False, "error": "No target Given.", "reason": "notarget"}

    # Optional don't allow self-target
    if "self" not in targetbypass:
        if bot_check_inlist(bot, target, botcom.instigator):
            return {"targetgood": False, "error": "This command does not allow you to target yourself.", "reason": "self"}

    # cannot target bots
    if "bot" not in targetbypass:
        if bot_check_inlist(bot, target, bot.nick):
            return {"targetgood": False, "error": "I am a bot and cannot be targeted.", "reason": "bot"}
    if "bots" not in targetbypass:
        if bot_check_inlist(bot, target, bot.nick):
            return {"targetgood": False, "error": nick_actual(bot, target) + " is a bot and cannot be targeted.", "reason": "bots"}

    # Not a valid user
    if "unknown" not in targetbypass:
        if not bot_check_inlist(bot, target, bot.memory["botdict"]["users"].keys()):
            sim_user, sim_num = [], []
            for user in bot.memory["botdict"]["users"].keys():
                similarlevel = similar(str(target).lower(), user.lower())
                if similarlevel >= .75:
                    sim_user.append(user)
                    sim_num.append(similarlevel)
            if sim_user != [] and sim_num != []:
                sim_num, sim_user = array_arrangesort(bot, sim_num, sim_user)
                closestmatch = spicemanip(bot, sim_user, 'reverse', "list")
                listnumb, relist = 1, []
                for item in closestmatch:
                    if listnumb <= 3:
                        relist.append(str(item))
                    listnumb += 1
                closestmatches = spicemanip(bot, relist, "andlist")
                targetgooderror = "It looks like you're trying to target someone! Did you mean: " + str(closestmatches) + "?"
            else:
                targetgooderror = "I am not sure who that is."
            return {"targetgood": False, "error": targetgooderror, "reason": "unknown"}

    # User offline
    if "offline" not in targetbypass:
        if not bot_check_inlist(bot, target, bot.memory["botdict"]["tempvals"]['servers_list'][botcom.server]['all_current_users']):
            return {"targetgood": False, "error": "It looks like " + nick_actual(bot, target) + " is offline right now!", "reason": "offline"}

    # Private Message
    if "privmsg" not in targetbypass:
        if botcom.channel_priv and not bot_check_inlist(bot, target, botcom.instigator):
            return {"targetgood": False, "error": "Leave " + nick_actual(bot, target) + " out of this private conversation!", "reason": "privmsg"}

    # not in the same channel
    if "diffchannel" not in targetbypass:
        if not botcom.channel_priv and bot_check_inlist(bot, target, bot.memory["botdict"]["tempvals"]['servers_list'][botcom.server]['all_current_users']):
            if not bot_check_inlist(bot, target, bot.memory["botdict"]["tempvals"]['servers_list'][botcom.server]['channels_list'][str(botcom.channel_current)]['current_users']):
                return {"targetgood": False, "error": "It looks like " + nick_actual(bot, target) + " is online right now, but in a different channel.", "reason": "diffchannel"}

    return targetgood


"""
Gif Searching
"""


def getGif(bot, searchdict):

    # list of defaults
    query_defaults = {
                    "query": None,
                    "searchnum": 'random',
                    "gifsearch": bot.memory["botdict"]["tempvals"]['valid_gif_api_dict'].keys(),
                    "gifsearchremove": ['gifme'],
                    "searchlimit": 'default',
                    "nsfw": False,
                    }

    # set defaults if they don't exist
    for key in query_defaults:
        if key not in searchdict.keys():
            searchdict[key] = query_defaults[key]
            if key == "gifsearch":
                for remx in query_defaults["gifsearchremove"]:
                    searchdict["gifsearch"].remove(remx)

    # Replace spaces in search query
    if not searchdict["query"]:
        return {"error": 'No Query to Search'}
    searchdict["searchquery"] = searchdict["query"].replace(' ', '%20')

    # set api usage
    if not isinstance(searchdict['gifsearch'], list):
        if str(searchdict['gifsearch']) in bot.memory["botdict"]["tempvals"]['valid_gif_api_dict'].keys():
            searchdict['gifsearch'] = [searchdict['gifsearch']]
        else:
            searchdict['gifsearch'] = bot.memory["botdict"]["tempvals"]['valid_gif_api_dict'].keys()
    else:
        for apis in searchdict['gifsearch']:
            if apis not in bot.memory["botdict"]["tempvals"]['valid_gif_api_dict'].keys():
                searchdict['gifsearch'].remove(apis)

    # Verify search limit
    if searchdict['searchlimit'] == 'default' or not isinstance(searchdict['searchlimit'], int):
        searchdict['searchlimit'] = 50

    # Random handling for searchnum
    if searchdict["searchnum"] == 'random':
        searchdict["searchnum"] = randint(0, searchdict['searchlimit'])

    # Make sure there is a valid input of query and search number
    if not searchdict["query"]:
        return {"error": 'No Query to Search'}

    if not str(searchdict["searchnum"]).isdigit():
        return {"error": 'No Search Number or Random Specified'}

    gifapiresults = []
    for currentapi in searchdict['gifsearch']:

        # url base
        url = str(bot.memory["botdict"]["tempvals"]['valid_gif_api_dict'][currentapi]['url'])
        # query
        url += str(bot.memory["botdict"]["tempvals"]['valid_gif_api_dict'][currentapi]['query']) + str(searchdict["searchquery"])
        # limit
        url += str(bot.memory["botdict"]["tempvals"]['valid_gif_api_dict'][currentapi]['limit']) + str(searchdict["searchlimit"])
        # nsfw search?
        if searchdict['nsfw']:
            url += str(bot.memory["botdict"]["tempvals"]['valid_gif_api_dict'][currentapi]['nsfw'])
        else:
            url += str(bot.memory["botdict"]["tempvals"]['valid_gif_api_dict'][currentapi]['sfw'])
        # api key
        url += str(bot.memory["botdict"]["tempvals"]['valid_gif_api_dict'][currentapi]['key']) + str(bot.memory["botdict"]["tempvals"]['valid_gif_api_dict'][currentapi]['apikey'])

        page = requests.get(url, headers=None)
        if page.status_code != 500 and page.status_code != 503:

            data = json.loads(urllib2.urlopen(url).read())

            results = data[bot.memory["botdict"]["tempvals"]['valid_gif_api_dict'][currentapi]['results']]
            resultsarray = []
            for result in results:
                cururl = result[bot.memory["botdict"]["tempvals"]['valid_gif_api_dict'][currentapi]['cururl']]
                if not str(cururl).startswith(tuple(gif_dontusesites)) and not str(cururl).endswith(tuple(gif_dontuseextensions)):
                    resultsarray.append(cururl)

            # make sure there are results
            resultsamount = len(resultsarray)
            if resultsarray != []:

                # Create Temp dict for every result
                tempresultnum = 0
                for tempresult in resultsarray:
                    tempresultnum += 1
                    tempdict = dict()
                    tempdict["returnnum"] = tempresultnum
                    tempdict["returnurl"] = tempresult
                    tempdict["gifapi"] = currentapi
                    gifapiresults.append(tempdict)

    if gifapiresults == []:
        return {"error": "No Results were found for '" + searchdict["query"] + "' in the " + str(spicemanip(bot, searchdict['gifsearch'], 'orlist')) + " api(s)"}

    random.shuffle(gifapiresults)
    random.shuffle(gifapiresults)
    gifdict = spicemanip(bot, gifapiresults, "random")

    # return dict
    gifdict['error'] = None
    return gifdict


"""
Networking
"""


def ipv4detect(bot, hostIP):
    pat = re.compile("\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}")
    test = pat.match(hostIP)
    return test


def find_used_port_in_range(bot, rangestart, rangeend, host):
    returnlist = []
    for i in range(rangestart, rangeend + 1):
        if is_port_in_use(i, host):
            returnlist.append(i)
    return returnlist


def find_unused_port_in_range(bot, rangestart, rangeend, host, ignorelist=[]):
    for i in range(rangestart, rangeend + 1):
        if i not in ignorelist:
            if not is_port_in_use(i, host):
                return i


def is_port_in_use(port, host):
    checkport = str(len(subprocess.Popen("netstat -lant | awk '{print $4}' | grep " + str(host) + ":" + str(port), shell=True, stdout=subprocess.PIPE).stdout.read()) > 0)
    if checkport == "True":
        return True
    elif checkport == "False":
        return False
    else:
        return False


"""
OS Functions
"""


def gitpull(bot, directory):
    if os.path.isdir(directory):
        stderr("Pulling " + str(directory) + "From Github.")
        try:
            g = git.cmd.Git(directory)
            g.pull()
        except Exception as e:
            stderr("Pulling " + str(directory) + "From Github Failed: " + str(e))
    else:
        stderr("Pulling " + str(directory) + "From Github Failed: Not a Valid Directory.")


def service_manip(bot, servicename, dowhat):
    if str(dowhat) not in ["start", "stop", "restart"]:
        return
    try:
        stderr(str(dowhat).title() + "ing " + str(servicename) + ".service.")
        os.system("sudo service " + str(servicename) + " " + str(dowhat))
    except Exception as e:
        stderr(str(dowhat).title() + "ing " + str(servicename) + ".service Failed: " + str(e))


def config_file_to_dict(bot, filetoread):

    newdict = dict()

    # Read configuration
    config = ConfigParser.ConfigParser()
    config.read(filetoread)

    for each_section in config.sections():

        if each_section not in newdict.keys():
            newdict[each_section] = dict()

            for (each_key, each_val) in config.items(each_section):
                if each_key not in newdict[each_section].keys():
                    newdict[each_section][each_key] = each_val
    return newdict


"""
dir listing
"""


def bot_list_directory(bot, botcom):
    botcom.directory_listing = []
    botcom.filefoldertype = []
    for filename in os.listdir(botcom.directory):
        botcom.directory_listing.append(filename)
        joindpath = os.path.join(botcom.directory, filename)
        if os.path.isfile(joindpath):
            botcom.filefoldertype.append("file")
        else:
            botcom.filefoldertype.append("folder")
    return botcom


"""
Time
"""


def humanized_time(countdownseconds):
    time = float(countdownseconds)
    if time == 0:
        return "just now"
    year = time // (365 * 24 * 3600)
    time = time % (365 * 24 * 3600)
    day = time // (24 * 3600)
    time = time % (24 * 3600)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minute = time // 60
    time %= 60
    second = time
    displaymsg = None
    timearray = ['year', 'day', 'hour', 'minute', 'second']
    for x in timearray:
        currenttimevar = eval(x)
        if currenttimevar >= 1:
            timetype = x
            if currenttimevar > 1:
                timetype = str(x+"s")
            if displaymsg:
                displaymsg = str(displaymsg + " " + str(int(currenttimevar)) + " " + timetype)
            else:
                displaymsg = str(str(int(currenttimevar)) + " " + timetype)
    if not displaymsg:
        return "just now"
    return displaymsg


def arrow_time(now, futuretime):
    a = arrow.get(now)
    b = arrow.get(futuretime)
    timecompare = (b.humanize(a, granularity='auto'))
    return timecompare


"""
Text Processing
"""


def bot_translate_process(bot, totranslate, translationtypes):

    # just in case
    if not isinstance(translationtypes, list):
        translationtypes = [translationtypes]

    for translationtype in translationtypes:

        if translationtype == "hyphen":
            totranslate = spicemanip(bot, totranslate, 0).replace(' ', '-')

        elif translationtype == "underscore":
            totranslate = spicemanip(bot, totranslate, 0).replace(' ', '_')

        elif translationtype == "ermahgerd":
            totranslate = trernslert(bot, totranslate)

        elif translationtype == "obscure":
            totranslate = text_obscure(bot, totranslate)

        elif translationtype == "piglatin":
            totranslate = text_piglatin(bot, totranslate)

        elif translationtype == "binaryinvert":
            totranslate = text_binary_swap(bot, totranslate)

        elif translationtype == "onetozero":
            totranslate = text_one_to_zero_swap(bot, totranslate)

        elif translationtype == "upper":
            totranslate = spicemanip(bot, totranslate, 0).upper()

        elif translationtype == "lower":
            totranslate = spicemanip(bot, totranslate, 0).lower()

    return totranslate


def text_obscure(bot, words):
    amountofletters = len(words)
    mystring = "*" * amountofletters
    return mystring


def text_piglatin(bot, words):
    if not isinstance(words, list):
        words = [words]
    rebuildarray = []
    for word in words:
        word = word.lower()
        first = word[:1]
        if first in ['a', 'e', 'i', 'o', 'u']:
            new_word = word + 'ay'
        else:
            new_word = word[1:] + first + 'ay'
        rebuildarray.append(new_word)
    words = spicemanip(bot, rebuildarray, 0)
    return words


def trernslert(bot, werds):
    terkerns = werds.split()
    er = ''
    for terk in terkerns:

        if terk.endswith(','):
            terk = re.sub(r"[,]+", '', terk)
            cermmer = 'true'
        else:
            cermmer = 'false'

        if terk.startswith('('):
            terk = re.sub(r"[(]+", '', terk)
            lerftperernthersers = 'true'
        else:
            lerftperernthersers = 'false'

        if terk.endswith(')'):
            terk = re.sub(r"[)]+", '', terk)
            rerghtperernthersers = 'true'
        else:
            rerghtperernthersers = 'false'

        if terk.endswith('%'):
            terk = re.sub(r"[%]+", '', terk)
            percernt = 'true'
        else:
            percernt = 'false'

        werd = ermergerd(terk)

        if lerftperernthersers == 'true':
            werd = str('(' + werd)

        if percernt == 'true':
            werd = str(werd + ' PERCERNT')

        if rerghtperernthersers == 'true':
            werd = str(werd + ')')

        if cermmer == 'true':
            werd = str(werd + ',')
        cermmer

        er = er + ' ' + werd
    return er


def ermergerd(w):
    w = w.strip().lower()
    derctshernerer = {'me': 'meh', 'you': 'u', 'are': 'er', "you're": "yer", "i'm": "erm", "i've": "erv", "my": "mah", "the": "da", "omg": "ermahgerd"}
    if w in derctshernerer:
        return derctshernerer[w].upper()
    else:
        w = re.sub(r"[\.,/;:!@#$%^&*\?)(]+", '', w)
        if w[0].isdigit():
            w = num2words(int(w))
        w = re.sub(r"tion", "shun", w)
        pat = r"[aeiouy]+"
        er = re.sub(pat, "er", w)
        if w.startswith('y'):
            er = 'y' + re.sub(pat, "er", w[1:])
        if w.endswith('e') and not w.endswith('ee') and len(w) > 3:
            er = re.sub(pat, "er", w[:-1])
        if w.endswith('ing'):
            er = re.sub(pat, "er", w[:-3]) + 'in'
        er = er[0] + er[1:].replace('y', 'er')
        er = er.replace('rr', 'r')
        return er.upper()


def text_one_to_zero_swap(bot, words):
    if not words or words == []:
        return "No input provided"
    if not isinstance(words, list):
        words = [words]
    words = spicemanip(bot, words, 0).split(" ")
    outputarray = []
    for word in words:
        if not isitbinary(word):
            word = text_binary_swap(bot, word)
        word = str(word).replace('1', '2')
        word = str(word).replace('0', '1')
        word = str(word).replace('2', '0')
        outputarray.append(str(word))
    outputarray = spicemanip(bot, outputarray, 0)
    return outputarray


def text_binary_swap(bot, words):
    if not words or words == []:
        return "No input provided"
    if not isinstance(words, list):
        words = [words]
    words = spicemanip(bot, words, 0).split(" ")
    outputarray = []
    for word in words:
        if isitbinary(word):
            word = bits2string(word) or 'error'
        else:
            word = string2bits(word) or 1
            word = spicemanip(bot, word, 0)
        outputarray.append(str(word))
    outputarray = spicemanip(bot, outputarray, 0)
    return outputarray


def unicode_string_cleanup(string):
    for r in (("\u2013", "-"), ("\u2019", "'"), ("\u2026", "...")):
        string = string.replace(*r)
    return string


"""
Small Functions
"""


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def countX(lst, x):
    count = 0
    for ele in lst:
        if (ele == x):
            count = count + 1
    return count


def isitbinary(string):
    p = set(string)
    s = {'0', '1'}
    if s == p or p == {'0'} or p == {'1'}:
        return True
    else:
        return False


def string2bits(s=''):
    return [bin(ord(x))[2:].zfill(8) for x in s]


def bits2string(b=None):
    return ''.join(chr(int(b[i*8:i*8+8], 2)) for i in range(len(b)//8))


"""
Database
"""


# Get a value
def get_database_value(bot, nick, databasekey):
    databasecolumn = str(databasekey)
    database_value = bot.db.get_nick_value(nick, databasecolumn) or 0
    return database_value


# set a value
def set_database_value(bot, nick, databasekey, value):
    databasecolumn = str(databasekey)
    bot.db.set_nick_value(nick, databasecolumn, value)


# set a value to None
def reset_database_value(bot, nick, databasekey):
    databasecolumn = str(databasekey)
    bot.db.set_nick_value(nick, databasecolumn, None)


# add or subtract from current value
def adjust_database_value(bot, nick, databasekey, value):
    oldvalue = get_database_value(bot, nick, databasekey) or 0
    databasecolumn = str(databasekey)
    bot.db.set_nick_value(nick, databasecolumn, int(oldvalue) + int(value))


# array stored in database length
def get_database_array_total(bot, nick, databasekey):
    array = get_database_value(bot, nick, databasekey) or []
    entriestotal = len(array)
    return entriestotal


# array stored in database, add or remove elements
def adjust_database_array(bot, nick, entries, databasekey, adjustmentdirection):
    if not isinstance(entries, list):
        entries = [entries]
    adjustarray = get_database_value(bot, nick, databasekey) or []
    adjustarraynew = []
    for x in adjustarray:
        adjustarraynew.append(x)
    reset_database_value(bot, nick, databasekey)
    adjustarray = []
    if adjustmentdirection == 'add':
        for y in entries:
            if y not in adjustarraynew:
                adjustarraynew.append(y)
    elif adjustmentdirection == 'del':
        for y in entries:
            if y in adjustarraynew:
                adjustarraynew.remove(y)
    for x in adjustarraynew:
        if x not in adjustarray:
            adjustarray.append(x)
    if adjustarray == []:
        reset_database_value(bot, nick, databasekey)
    else:
        set_database_value(bot, nick, databasekey, adjustarray)


# this function inputs list information if not there
def database_initialize(bot, nick, array, database):
    databasekey = str(database)
    existingarray = get_database_value(bot, bot.nick, databasekey)
    if not existingarray:
        arraycount = (len(array) - 1)
        i = 0
        while (i <= arraycount):
            inputstring = array[i]
            adjust_database_array(bot, bot.nick, inputstring, databasekey, 'add')
            i = i + 1


# Database Users
def get_user_dict(bot, dynamic_class, nick, dictkey):

    # check that db list is there
    if not hasattr(dynamic_class, 'userdb'):
        dynamic_class.userdb = class_create('userdblist')
    if not hasattr(dynamic_class.userdb, 'list'):
        dynamic_class.userdb.list = []

    returnvalue = 0

    # check if nick has been pulled from db already
    if nick not in dynamic_class.userdb.list:
        dynamic_class.userdb.list.append(nick)
        nickdict = get_database_value(bot, nick, dynamic_class.default) or dict()
        createuserdict = str("dynamic_class.userdb." + nick + " = nickdict")
        exec(createuserdict)
    else:
        if not hasattr(dynamic_class.userdb, nick):
            nickdict = dict()
        else:
            nickdict = eval('dynamic_class.userdb.' + nick)

    if dictkey in nickdict.keys():
        returnvalue = nickdict[dictkey]
    else:
        nickdict[dictkey] = 0
        returnvalue = 0

    return returnvalue


# set a value
def set_user_dict(bot, dynamic_class, nick, dictkey, value):
    currentvalue = get_user_dict(bot, dynamic_class, nick, dictkey)
    nickdict = eval('dynamic_class.userdb.' + nick)
    nickdict[dictkey] = value


# reset a value
def reset_user_dict(bot, dynamic_class, nick, dictkey):
    currentvalue = get_user_dict(bot, dynamic_class, nick, dictkey)
    nickdict = eval('dynamic_class.userdb.' + nick)
    if dictkey in nickdict:
        del nickdict[dictkey]


# add or subtract from current value
def adjust_user_dict(bot, dynamic_class, nick, dictkey, value):
    oldvalue = get_user_dict(bot, dynamic_class, nick, dictkey)
    if not str(oldvalue).isdigit():
        oldvalue = 0
    nickdict = eval('dynamic_class.userdb.' + nick)
    nickdict[dictkey] = oldvalue + value


# Save all database users in list
def save_user_dicts(bot, dynamic_class):

    # check that db list is there
    if not hasattr(dynamic_class, 'userdb'):
        dynamic_class.userdb = class_create('userdblist')
    if not hasattr(dynamic_class.userdb, 'list'):
        dynamic_class.userdb.list = []

    for nick in dynamic_class.userdb.list:
        if not hasattr(dynamic_class.userdb, nick):
            nickdict = dict()
        else:
            nickdict = eval('dynamic_class.userdb.' + nick)
        set_database_value(bot, nick, dynamic_class.default, nickdict)


# add or subtract from current value
def adjust_user_dict_array(bot, dynamic_class, nick, dictkey, entries, adjustmentdirection):
    if not isinstance(entries, list):
        entries = [entries]
    oldvalue = get_user_dict(bot, dynamic_class, nick, dictkey)
    nickdict = eval('dynamic_class.userdb.' + nick)
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


# get values from other bots
def get_nick_value_api(bot, botname, nick, longevity, sortingkey, usekey):
    try:
        if longevity == 'long':
            botvaltime = bot.memory["altbots"][botname]["users"][nick][sortingkey][usekey]["value"]
        elif longevity == 'temp':
            botvaltime = bot.memory["altbots"][botname]["tempvals"]["uservals"][nick][sortingkey][usekey]["value"]
    except Exception as e:
        botvaltime = None
    return botvaltime


# get nick value from bot.memory
def get_nick_value(bot, nick, longevity, sortingkey, usekey):

    # verify nick dict exists
    if longevity == 'long':
        if nick not in bot.memory["botdict"]["users"].keys():
            bot.memory["botdict"]["users"][nick] = dict()
    elif longevity == 'temp':
        if nick not in bot.memory["botdict"]["tempvals"]["uservals"].keys():
            bot.memory["botdict"]["tempvals"]["uservals"][nick] = dict()

    # Verify sortingkey exists
    if longevity == 'long':
        if sortingkey not in bot.memory["botdict"]["users"][nick].keys():
            bot.memory["botdict"]["users"][nick][sortingkey] = dict()
    elif longevity == 'temp':
        if sortingkey not in bot.memory["botdict"]["tempvals"]["uservals"][nick].keys():
            bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey] = dict()

    # Verify usekey exists
    if longevity == 'long':
        if usekey not in bot.memory["botdict"]["users"][nick][sortingkey].keys():
            bot.memory["botdict"]["users"][nick][sortingkey][usekey] = dict()
        if not isinstance(bot.memory["botdict"]["users"][nick][sortingkey][usekey], dict):
            oldvalue = bot.memory["botdict"]["users"][nick][sortingkey][usekey]
            bot.memory["botdict"]["users"][nick][sortingkey][usekey] = dict()
            bot.memory["botdict"]["users"][nick][sortingkey][usekey]["value"] = oldvalue
    elif longevity == 'temp':
        if usekey not in bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey].keys():
            bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey] = dict()
        if not isinstance(bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey], dict):
            oldvalue = bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey]
            bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey] = dict()
            bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey]["value"] = oldvalue

    # Get the value
    if longevity == 'long':
        if "value" not in bot.memory["botdict"]["users"][nick][sortingkey][usekey].keys():
            bot.memory["botdict"]["users"][nick][sortingkey][usekey]["value"] = None
        if "timestamp" not in bot.memory["botdict"]["users"][nick][sortingkey][usekey].keys():
            bot.memory["botdict"]["users"][nick][sortingkey][usekey]["timestamp"] = 0
        return bot.memory["botdict"]["users"][nick][sortingkey][usekey]["value"]
    elif longevity == 'temp':
        if "value" not in bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey].keys():
            bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey]["value"] = None
        if "timestamp" not in bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey].keys():
            bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey]["timestamp"] = 0
        return bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey]["value"]


def adjust_nick_value(bot, nick, longevity, sortingkey, usekey, value):
    oldvalue = get_nick_value(bot, nick, longevity, sortingkey, usekey) or 0
    set_nick_value(bot, nick, longevity, sortingkey, usekey, int(oldvalue) + int(value))


# set nick value in bot.memory
def set_nick_value(bot, nick, longevity, sortingkey, usekey, value):

    # verify nick dict exists
    if longevity == 'long':
        if nick not in bot.memory["botdict"]["users"].keys():
            bot.memory["botdict"]["users"][nick] = dict()
    elif longevity == 'temp':
        if nick not in bot.memory["botdict"]["tempvals"]["uservals"].keys():
            bot.memory["botdict"]["tempvals"]["uservals"][nick] = dict()

    # Verify sortingkey exists
    if longevity == 'long':
        if sortingkey not in bot.memory["botdict"]["users"][nick].keys():
            bot.memory["botdict"]["users"][nick][sortingkey] = dict()
    elif longevity == 'temp':
        if sortingkey not in bot.memory["botdict"]["tempvals"]["uservals"][nick].keys():
            bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey] = dict()

    # Verify usekey exists
    if longevity == 'long':
        if usekey not in bot.memory["botdict"]["users"][nick][sortingkey].keys():
            bot.memory["botdict"]["users"][nick][sortingkey][usekey] = dict()
        if not isinstance(bot.memory["botdict"]["users"][nick][sortingkey][usekey], dict):
            oldvalue = bot.memory["botdict"]["users"][nick][sortingkey][usekey]
            bot.memory["botdict"]["users"][nick][sortingkey][usekey] = dict()
            bot.memory["botdict"]["users"][nick][sortingkey][usekey]["value"] = oldvalue
    elif longevity == 'temp':
        if usekey not in bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey].keys():
            bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey] = dict()
        if not isinstance(bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey], dict):
            oldvalue = bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey]
            bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey] = dict()
            bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey]["value"] = oldvalue

    # Se the value
    currtime = time.time()
    if longevity == 'long':
        bot.memory["botdict"]["users"][nick][sortingkey][usekey]["value"] = value
        bot.memory["botdict"]["users"][nick][sortingkey][usekey]["timestamp"] = currtime
    elif longevity == 'temp':
        bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey]["value"] = value
        bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey]["timestamp"] = currtime


# set nick value in bot.memory
def reset_nick_value(bot, nick, longevity, sortingkey, usekey):

    # if str(bot.nick).endswith("dev"):
    #    usekey = usekey + "_dev"

    # verify nick dict exists
    if longevity == 'long':
        if nick not in bot.memory["botdict"]["users"].keys():
            bot.memory["botdict"]["users"][nick] = dict()
    elif longevity == 'temp':
        if nick not in bot.memory["botdict"]["tempvals"]["uservals"].keys():
            bot.memory["botdict"]["tempvals"]["uservals"][nick] = dict()

    # Verify sortingkey exists
    if longevity == 'long':
        if sortingkey not in bot.memory["botdict"]["users"][nick].keys():
            bot.memory["botdict"]["users"][nick][sortingkey] = dict()
    elif longevity == 'temp':
        if sortingkey not in bot.memory["botdict"]["tempvals"]["uservals"][nick].keys():
            bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey] = dict()

    # Verify usekey exists
    if longevity == 'long':
        if usekey not in bot.memory["botdict"]["users"][nick][sortingkey].keys():
            bot.memory["botdict"]["users"][nick][sortingkey][usekey] = dict()
        if not isinstance(bot.memory["botdict"]["users"][nick][sortingkey][usekey], dict):
            oldvalue = bot.memory["botdict"]["users"][nick][sortingkey][usekey]
            bot.memory["botdict"]["users"][nick][sortingkey][usekey] = dict()
            bot.memory["botdict"]["users"][nick][sortingkey][usekey]["value"] = oldvalue
    elif longevity == 'temp':
        if usekey not in bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey].keys():
            bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey] = dict()
        if not isinstance(bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey], dict):
            oldvalue = bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey]
            bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey] = dict()
            bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey]["value"] = oldvalue

    # Reset the value
    currtime = time.time()
    if longevity == 'long':
        bot.memory["botdict"]["users"][nick][sortingkey][usekey]["value"] = None
        bot.memory["botdict"]["users"][nick][sortingkey][usekey]["timestamp"] = currtime
    elif longevity == 'temp':
        bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey]["value"] = None
        bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey]["timestamp"] = currtime


def adjust_nick_array(bot, nick, longevity, sortingkey, usekey, values, direction):

    if not isinstance(values, list):
        values = [values]

    oldvalues = get_nick_value(bot, nick, longevity, sortingkey, usekey) or []

    # startup entries
    if direction == 'startup':
        if longevity == 'long':
            if oldvalues == []:
                direction == 'add'
            else:
                return
        elif longevity == 'temp':
            if oldvalues == []:
                direction == 'add'
            else:
                return

    # adjust
    for value in values:
        if longevity == 'long':
            if direction == 'add':
                if value not in oldvalues:
                    oldvalues.append(value)
            elif direction == 'startup':
                if value not in oldvalues:
                    oldvalues.append(value)
            elif direction in ['del', 'remove']:
                if value in oldvalues:
                    oldvalues.remove(value)
        elif longevity == 'temp':
            if direction == 'add':
                if value not in oldvalues:
                    oldvalues.append(value)
            elif direction == 'startup':
                if value not in oldvalues:
                    oldvalues.append(value)
            elif direction in ['del', 'remove']:
                if value in oldvalues:
                    oldvalues.remove(value)

    set_nick_value(bot, nick, longevity, sortingkey, usekey, oldvalues)


"""
On Screen Text
"""


def osd(bot, target_array, text_type_array, text_array):

    # if text_array is a string, make it an array
    textarraycomplete = []
    if not isinstance(text_array, list):
        textarraycomplete.append(text_array)
    else:
        for x in text_array:
            textarraycomplete.append(x)

    # if target_array is a string, make it an array
    texttargetarray = []
    if not isinstance(target_array, list):
        if not str(target_array).startswith("#"):
            target_array = nick_actual(bot, str(target_array))
        texttargetarray.append(target_array)
    else:
        for target in target_array:
            if not str(target).startswith("#"):
                target = nick_actual(bot, str(target))
            texttargetarray.append(target)

    # Handling for text_type
    texttypearray = []
    if not isinstance(text_type_array, list):
        for i in range(len(texttargetarray)):
            texttypearray.append(str(text_type_array))
    else:
        for x in text_type_array:
            texttypearray.append(str(x))
    if texttypearray == []:
        texttypearray.append('say')
    text_array_common = max(((item, texttypearray.count(item)) for item in set(texttypearray)), key=lambda a: a[1])[0]

    # make sure len() equals
    if len(texttargetarray) > len(texttypearray):
        while len(texttargetarray) > len(texttypearray):
            texttypearray.append(text_array_common)
    elif len(texttargetarray) < len(texttypearray):
        while len(texttargetarray) < len(texttypearray):
            texttargetarray.append('osd_error_handle')

    # Rebuild the text array to ensure string lengths

    for target, text_type in zip(texttargetarray, texttypearray):

        if target == 'osd_error_handle':
            dont_say_it = 1
        else:

            # Text array
            temptextarray = []

            # Notice handling
            if text_type == 'notice':
                temptextarray.insert(0, target + ", ")
                # temptextarray.append(target + ", ")
            for part in textarraycomplete:
                temptextarray.append(part)

            # 'say' can equal 'priv'
            if text_type == 'say' and not str(target).startswith("#"):
                text_type = 'priv'

            # Make sure no individual string ins longer than it needs to be
            currentstring = ''
            texttargetarray = []
            for textstring in temptextarray:
                if len(textstring) > 420:
                    chunks = textstring.split()
                    for chunk in chunks:
                        if currentstring == '':
                            currentstring = chunk
                        else:
                            tempstring = str(currentstring + " " + chunk)
                            if len(tempstring) <= 420:
                                currentstring = tempstring
                            else:
                                texttargetarray.append(currentstring)
                                currentstring = chunk
                    if currentstring != '':
                        texttargetarray.append(currentstring)
                else:
                    texttargetarray.append(textstring)

            # Split text to display nicely
            combinedtextarray = []
            currentstring = ''
            for textstring in texttargetarray:
                if currentstring == '':
                    currentstring = textstring
                elif len(textstring) > 420:
                    if currentstring != '':
                        combinedtextarray.append(currentstring)
                        currentstring = ''
                    combinedtextarray.append(textstring)
                else:
                    tempstring = currentstring + "   " + textstring
                    if len(tempstring) <= 420:
                        currentstring = tempstring
                    else:
                        combinedtextarray.append(currentstring)
                        currentstring = textstring
            if currentstring != '':
                combinedtextarray.append(currentstring)

            # display
            textparts = len(combinedtextarray)
            textpartsleft = textparts
            for combinedline in combinedtextarray:
                if text_type == 'action' and textparts == textpartsleft:
                    bot.action(combinedline, target)
                elif str(target).startswith("#"):
                    bot.msg(target, combinedline)
                elif text_type == 'notice' or text_type == 'priv':
                    bot.notice(combinedline, target)
                elif text_type == 'say':
                    bot.say(combinedline)
                else:
                    bot.say(combinedline)
                textpartsleft = textpartsleft - 1


"""
Array/List/String Manipulation
"""


# Hub
def spicemanip(bot, inputs, outputtask, output_type='default'):

    # TODO 'this*that' or '1*that' replace either all strings matching, or an index value
    # TODO reverse sort z.sort(reverse = True)
    # list.extend adds lists to eachother

    mainoutputtask, suboutputtask = None, None

    # Input needs to be a list, but don't split a word into letters
    if not inputs:
        inputs = []
    if not isinstance(inputs, list):
        inputs = list(inputs.split(" "))
        inputs = [x for x in inputs if x and x not in ['', ' ']]
        inputs = [inputspart.strip() for inputspart in inputs]

    # Create return
    if outputtask == 'create':
        return inputs

    # Make temparray to preserve original order
    temparray = []
    for inputpart in inputs:
        temparray.append(inputpart)
    inputs = temparray

    # Convert outputtask to standard
    if outputtask in [0, 'complete']:
        outputtask = 'string'
    elif outputtask == 'index':
        mainoutputtask = inputs[1]
        suboutputtask = inputs[2]
        inputs = inputs[0]
    elif str(outputtask).isdigit():
        mainoutputtask, outputtask = int(outputtask), 'number'
    elif "^" in str(outputtask):
        mainoutputtask = str(outputtask).split("^", 1)[0]
        suboutputtask = str(outputtask).split("^", 1)[1]
        outputtask = 'rangebetween'
        if int(suboutputtask) < int(mainoutputtask):
            mainoutputtask, suboutputtask = suboutputtask, mainoutputtask
    elif str(outputtask).startswith("split_"):
        mainoutputtask = str(outputtask).replace("split_", "")
        outputtask = 'split'
    elif str(outputtask).endswith(tuple(["!", "+", "-", "<", ">"])):
        mainoutputtask = str(outputtask)
        if str(outputtask).endswith("!"):
            outputtask = 'exclude'
        if str(outputtask).endswith("+"):
            outputtask = 'incrange_plus'
        if str(outputtask).endswith("-"):
            outputtask = 'incrange_minus'
        if str(outputtask).endswith(">"):
            outputtask = 'excrange_plus'
        if str(outputtask).endswith("<"):
            outputtask = 'excrange_minus'
        for r in (("!", ""), ("+", ""), ("-", ""), ("<", ""), (">", "")):
            mainoutputtask = mainoutputtask.replace(*r)
    if mainoutputtask == 'last':
        mainoutputtask = len(inputs)

    if outputtask == 'string':
        returnvalue = inputs
    else:
        returnvalue = eval('spicemanip_' + outputtask + '(bot, inputs, outputtask, mainoutputtask, suboutputtask)')

    # default return if not specified
    if output_type == 'default':
        if outputtask in [
                            'string', 'number', 'rangebetween', 'exclude', 'random',
                            'incrange_plus', 'incrange_minus', 'excrange_plus', 'excrange_minus'
                            ]:
            output_type = 'string'
        elif outputtask in ['count']:
            output_type = 'dict'

    # verify output is correct
    if output_type == 'return':
        return returnvalue
    if output_type == 'string':
        if isinstance(returnvalue, list):
            returnvalue = ' '.join(returnvalue)
    elif output_type in ['list', 'array']:
        if not isinstance(returnvalue, list):
            returnvalue = list(returnvalue.split(" "))
            returnvalue = [x for x in returnvalue if x and x not in ['', ' ']]
            returnvalue = [inputspart.strip() for inputspart in returnvalue]
    return returnvalue


# compare 2 lists, based on the location of an index item, passthrough needs to be [indexitem, arraytoindex, arraytocompare]
def spicemanip_index(bot, indexitem, outputtask, arraytoindex, arraytocompare):
    item = ''
    for x, y in zip(arraytoindex, arraytocompare):
        if x == indexitem:
            item = y
    return item


# split list by string
def spicemanip_split(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    split_array = []
    restring = ' '.join(inputs)
    if mainoutputtask not in inputs:
        split_array = [restring]
    else:
        split_array = restring.split(mainoutputtask)
    split_array = [x for x in split_array if x and x not in ['', ' ']]
    split_array = [inputspart.strip() for inputspart in split_array]
    if split_array == []:
        split_array = [[]]
    return split_array


# dedupe list
def spicemanip_dedupe(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    newlist = []
    for inputspart in inputs:
        if inputspart not in newlist:
            newlist.append(inputspart)
    return newlist


# Sort list
def spicemanip_sort(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    return sorted(inputs)


# reverse sort list
def spicemanip_rsort(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    return sorted(inputs)[::-1]


# count items in list, return dictionary
def spicemanip_count(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    returndict = dict()
    if inputs == []:
        return returndict
    uniqueinputitems, uniquecount = [], []
    for inputspart in inputs:
        if inputspart not in uniqueinputitems:
            uniqueinputitems.append(inputspart)
    for uniqueinputspart in uniqueinputitems:
        count = 0
        for ele in inputs:
            if (ele == uniqueinputspart):
                count += 1
        uniquecount.append(count)
    for inputsitem, unumber in zip(uniqueinputitems, uniquecount):
        returndict[inputsitem] = unumber
    return returndict


# random item from list
def spicemanip_random(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    randomselectlist = []
    for temppart in inputs:
        randomselectlist.append(temppart)
    while len(randomselectlist) > 1:
        random.shuffle(randomselectlist)
        randomselect = randomselectlist[random.randint(0, len(randomselectlist) - 1)]
        randomselectlist.remove(randomselect)
    randomselect = randomselectlist[0]
    return randomselect


# remove random item from list
def spicemanip_exrandom(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return []
    randremove = spicemanip_random(bot, inputs, outputtask, mainoutputtask, suboutputtask)
    inputs.remove(randremove)
    return inputs


# Convert list into lowercase
def spicemanip_lower(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    return [inputspart.lower() for inputspart in inputs]


# Convert list to uppercase
def spicemanip_upper(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    return [inputspart.upper() for inputspart in inputs]


# Convert list to uppercase
def spicemanip_title(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    return [inputspart.title() for inputspart in inputs]


# Reverse List Order
def spicemanip_reverse(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return []
    return inputs[::-1]


# comma seperated list
def spicemanip_list(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    return ', '.join(str(x) for x in inputs)


# comma seperated list with and
def spicemanip_andlist(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    if len(inputs) < 2:
        return ' '.join(inputs)
    lastentry = str("and " + str(inputs[len(inputs) - 1]))
    del inputs[-1]
    inputs.append(lastentry)
    if len(inputs) == 2:
        return ' '.join(inputs)
    return ', '.join(str(x) for x in inputs)


# comma seperated list with or
def spicemanip_orlist(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    if len(inputs) < 2:
        return ' '.join(inputs)
    lastentry = str("or " + str(inputs[len(inputs) - 1]))
    del inputs[-1]
    inputs.append(lastentry)
    if len(inputs) == 2:
        return ' '.join(inputs)
    return ', '.join(str(x) for x in inputs)


# exclude number
def spicemanip_exclude(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    del inputs[int(mainoutputtask) - 1]
    return ' '.join(inputs)


# Convert list to string
def spicemanip_string(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    return ' '.join(inputs)


# Get number item from list
def spicemanip_number(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    elif len(inputs) == 1:
        return inputs[0]
    elif int(mainoutputtask) > len(inputs) or int(mainoutputtask) < 0:
        return ''
    else:
        return inputs[int(mainoutputtask) - 1]


# Get Last item from list
def spicemanip_last(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    return inputs[len(inputs) - 1]


# range between items in list
def spicemanip_rangebetween(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    if not str(mainoutputtask).isdigit() or not str(suboutputtask).isdigit():
        return ''
    mainoutputtask, suboutputtask = int(mainoutputtask), int(suboutputtask)
    if suboutputtask == mainoutputtask:
        return spicemanip_number(bot, inputs, outputtask, mainoutputtask, suboutputtask)
    if suboutputtask < mainoutputtask:
        return []
    if mainoutputtask < 0:
        mainoutputtask = 1
    if suboutputtask > len(inputs):
        suboutputtask = len(inputs)
    newlist = []
    for i in range(mainoutputtask, suboutputtask + 1):
        newlist.append(str(spicemanip_number(bot, inputs, outputtask, i, suboutputtask)))
    if newlist == []:
        return ''
    return ' '.join(newlist)


# Forward Range includes index number
def spicemanip_incrange_plus(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    return spicemanip_rangebetween(bot, inputs, outputtask, int(mainoutputtask), len(inputs))


# Reverse Range includes index number
def spicemanip_incrange_minus(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    return spicemanip_rangebetween(bot, inputs, outputtask, 1, int(mainoutputtask))


# Forward Range excludes index number
def spicemanip_excrange_plus(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    return spicemanip_rangebetween(bot, inputs, outputtask, int(mainoutputtask) + 1, len(inputs))


# Reverse Range excludes index number
def spicemanip_excrange_minus(bot, inputs, outputtask, mainoutputtask, suboutputtask):
    if inputs == []:
        return ''
    return spicemanip_rangebetween(bot, inputs, outputtask, 1, int(mainoutputtask) - 1)


def array_arrangesort(bot, sortbyarray, arrayb):
    sortbyarray, arrayb = (list(x) for x in zip(*sorted(zip(sortbyarray, arrayb), key=itemgetter(0))))
    return sortbyarray, arrayb


"""
# Empty Classes
"""


def class_create(classname):
    compiletext = """
        def __init__(self):
            self.default = str(self.__class__.__name__)
        def __repr__(self):
            return repr(self.default)
        def __str__(self):
            return str(self.default)
        def __iter__(self):
            return str(self.default)
        pass
        """
    exec(compile("class class_" + str(classname) + ": " + compiletext, "", "exec"))
    newclass = eval('class_'+classname+"()")
    return newclass
