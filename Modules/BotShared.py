#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
from sopel import module, tools
import sopel.module
from sopel.module import commands, nickname_commands, event, rule, OP, ADMIN, VOICE, HALFOP, OWNER, thread, priority, example
from sopel.tools import Identifier, stderr
from sopel.tools.time import get_timezone, format_time

# imports for system and OS access, directories
import os
from os.path import exists
import sys
import socket
import threading
import subprocess

# Additional imports
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
from fake_useragent import UserAgent
import praw
from prawcore import NotFound
import twitter
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
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


# user agent and header
ua = UserAgent()
header = {'User-Agent': str(ua.chrome)}


# Ensure Encoding
reload(sys)
sys.setdefaultencoding('utf-8')

"""
Variables # TODO add to botdict
"""


osd_limit = 420  # Ammount of text allowed to display per line

valid_com_types = ['simple', 'fillintheblank', 'targetplusreason', 'sayings', "readfromfile", "readfromurl", "ascii_art", "gif", "translate", "responses"]


"""
Bot Dictionaries
"""

bot_dict = {
                # Some values don't get saved to the database, but stay in memory
                "tempvals": {

                            # Indicate if we need to pull the dict from the database
                            "dict_loaded": False,

                            "sock": None,

                            # Time The Bot started last
                            "uptime": None,

                            # Configs directory
                            "config_dir": None,

                            # External Config
                            "ext_conf": {},

                            # Gif API
                            "valid_gif_api_dict": {},

                            # Loaded configs
                            "dict_commands": {},
                            "dict_commands_loaded": [],

                            # text files
                            "txt_files": {},
                            "txt_files_loaded": [],

                            # server the bot is connected to
                            "server": False,
                            "servername": False,

                            # Channels
                            "channels_list": {},

                            # Current Users
                            "all_current_users": [],

                            # offline users
                            "offline_users": [],

                            # Bots
                            "bots_list": {},
                            "bot_admins": [],
                            "bot_owners": [],

                            # temp user values
                            "uservals": {},

                            # Automod
                            "automod": {
                                        "antiflood": [],
                                        },

                            # End of Temp Vals
                            },

                # Static content
                "static": {
                            "bots": {
                                    "update_text": {
                                                    "spiceRPG": "My Dungeon Master, $instigator, hath commandeth me to performeth an update from the Hub of Gits. I shall return post haste!",
                                                    "spiceRPGdev": "My Dungeon Master, $instigator, hath commandeth me to performeth an update from the Hub of Gits. I shall return post haste!",
                                                    },
                                    "restart_text": {
                                                    "spiceRPG": "My Dungeon Master, $instigator, hath commandeth me to restart. I shall return post haste!",
                                                    "spiceRPGdev": "My Dungeon Master, $instigator, hath commandeth me to restart. I shall return post haste!",
                                                    },
                                    },

                            },

                # Users lists
                "users": {},

                # Channels
                "channels_list": {},

                }

# valid commands that the bot will reply to by name
valid_botnick_commands = {
                            "github": {
                                        'privs': [],
                                        },
                            "docs": {
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

mode_dict_alias = {
                    "o": "OP",
                    "v": "VOICE",
                    "h": "HALFOP",
                    "a": "ADMIN",
                    "q": "OWNER",
                    }


gif_dontusesites = [
                        "http://forgifs.com", "http://a.dilcdn.com", "http://www.bestgifever.com",
                        "http://s3-ec.buzzfed.com", "http://i.minus.com", "http://fap.to", "http://prafulla.net",
                        "http://3.bp.blogspot.com"
                        ]

gif_dontuseextensions = ['.jpg', '.png']


"""
Sock
"""


sock = None
PORT = 8080  # SOPL
TARGET = '#spicebottest'


"""
Bot Startup
"""


# order of operations for startup
def botdict_open(bot):

    if "botdict_loaded" in bot.memory:
        return

    bot.memory["botdict"] = botdict_setup_open(bot)

    if not bot.memory["botdict"]["tempvals"]["uptime"]:
        bot.memory["botdict"]["tempvals"]["uptime"] = datetime.datetime.utcnow()

    # load external config file
    botdict_setup_external_config(bot)

    # open the sockmsg feature
    bot_setup_sockmsg(bot)

    # Gif API
    botdict_setup_gif_api_access(bot)

    # Server connected to, default assumes ZNC bouncer configuration
    # this can be tweaked below
    botdict_setup_server(bot)

    # Channel Listing
    botdict_setup_channels(bot)

    # Bot configs
    botdict_setup_bots(bot)

    # users
    botdict_setup_users(bot)

    # Text Files
    bot_read_txt_files(bot)

    # dictionary commands
    dict_command_configs(bot)

    # iniital privacy sweep
    bot_setup_privacy_sweep(bot)

    # use this to prevent bot usage if the above isn't done loading
    bot.memory["botdict_loaded"] = True

    # save dictionary now
    botdict_save(bot)


# open dictionary, and import saved values from database
def botdict_setup_open(bot):

    # open global dict
    global bot_dict
    botdict = bot_dict

    # don't pull from database if already open
    if not botdict["tempvals"]["dict_loaded"]:
        opendict = botdict.copy()
        dbbotdict = get_database_value(bot, bot.nick, 'bot_dict') or dict()
        opendict = merge_botdict(opendict, dbbotdict)
        botdict.update(opendict)
        botdict["tempvals"]['dict_loaded'] = True
    return botdict


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


# externally stored config
def botdict_setup_external_config(bot):

    # Don't load commands if already loaded
    if bot.memory["botdict"]["tempvals"]['ext_conf'] != dict():
        return

    # Loop through external config file
    config = ConfigParser.ConfigParser()
    config.read("/home/spicebot/spicebot.conf")
    for each_section in config.sections():

        if each_section not in bot.memory["botdict"]["tempvals"]['ext_conf'].keys():
            bot.memory["botdict"]["tempvals"]['ext_conf'][each_section] = dict()

        for (each_key, each_val) in config.items(each_section):

            if each_key not in bot.memory["botdict"]["tempvals"]['ext_conf'][each_section].keys():
                bot.memory["botdict"]["tempvals"]['ext_conf'][each_section][each_key] = each_val


# setup listening socket
def bot_setup_sockmsg(bot):

    # Don't load sock if already loaded
    if bot.memory["botdict"]["tempvals"]['sock']:
        return

    bot.memory["botdict"]["tempvals"]['sock'] = socket.socket()  # the default socket types should be fine for sending text to localhost
    try:
        bot.memory["botdict"]["tempvals"]['sock'].bind(('0.0.0.0', PORT))
        stderr("Loaded socket on port %s" % (PORT))
    except socket.error as msg:
        stderr("Error loading socket on port %s: %s (%s)" % (PORT, str(msg[0]), str(msg[1])))
        return
    find_unused_port_in_range(bot, 8080, 9090)
    bot.memory["botdict"]["tempvals"]['sock'].listen(5)
    conn, addr = bot.memory["botdict"]["tempvals"]['sock'].accept()
    threading.Thread(target=sock_receiver, args=(conn, bot), name='sockmsg-listener').start()


def find_unused_port_in_range(bot, rangestart, rangeend):
    for i in range(rangestart, rangeend + 1):
        if is_port_in_use(i):
            bot.msg("#spicebottest", str(i))
            return i


def is_port_in_use(port):
    return str(len(subprocess.Popen("netstat -lant | awk '{print $4}' | grep 0.0.0.0:" + str(port), shell=True, stdout=subprocess.PIPE).stdout.read()) > 0)


def sock_receiver(conn, bot):
    buffer = ''
    while True:
        data = conn.recv(2048)
        buffer += data
        if not data:
            conn.close()
            break
        if '\n' in buffer:
            data, _, buffer = buffer.rpartition('\n')
            sayit(bot, data)
    sayit(bot, buffer)


def sayit(bot, data):
    for line in data.splitlines():
        bot.say("[sockmsg] %s" % line, TARGET)


# gif searching api
def botdict_setup_gif_api_access(bot):

    # Don't load commands if already loaded
    if bot.memory["botdict"]["tempvals"]['valid_gif_api_dict'] != dict():
        return

    valid_gif_api_dict = {
                            "giphy": {
                                        "url": "http://api.giphy.com/v1/gifs/search?",
                                        "query": 'q=',
                                        "limit": '&limit=',
                                        "id": None,
                                        "api_id": None,
                                        "key": "&api_key=",
                                        "apikey": bot.memory["botdict"]["tempvals"]['ext_conf']["giphy"]["apikey"],
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
                                        "apikey": bot.memory["botdict"]["tempvals"]['ext_conf']["tenor"]["apikey"],
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
                                        "apikey": None,
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
                                        "apikey": 'rX7kbMzkGu7WJwvG',
                                        "nsfw": '&sfw=false',
                                        "sfw": '&sfw=true',
                                        "results": 'data',
                                        "cururl": 'link',
                                        },
                            }
    bot.memory["botdict"]["tempvals"]['valid_gif_api_dict'] = valid_gif_api_dict


# servername
def botdict_setup_server(bot):

    # if host is set in the config without a bouncer, uncomment the next two lines:
    # bot.memory["botdict"]["tempvals"]['server'] = bot.config.core.host
    # return

    # The server the bot is connected to. Sopel limit is one
    # this detects the use of an IRC bouncer like ZNC
    # This is a custom function for this bot's connection
    if not bot.memory["botdict"]["tempvals"]['server']:
        if ipv4detect(bot, bot.config.core.host):
            servername = str(bot.config.core.user.split("/", 1)[1])
            if servername == 'SpiceBot':
                server = 'irc.spicebot.net'
            elif servername == 'Freenode':
                server = 'irc.freenode.net'
            else:
                server = bot.config.core.host
        else:
            server = bot.config.core.host
        bot.memory["botdict"]["tempvals"]['server'] = server

    if not bot.memory["botdict"]["tempvals"]['servername']:
        if ipv4detect(bot, bot.config.core.host):
            servername = str(bot.config.core.user.split("/", 1)[1])
            if servername not in tuple(["SpiceBot", "Freenode"]):
                servername = bot.config.core.host
        else:
            servername = bot.config.core.host
        bot.memory["botdict"]["tempvals"]['servername'] = servername


# create listing for channels the bot is in
def botdict_setup_channels(bot):

    # All channels the bot is in
    if bot.memory["botdict"]["tempvals"]['channels_list'].keys() == []:
        for channel in bot.channels:

            # curent channels
            if str(channel) not in bot.memory["botdict"]["tempvals"]['channels_list'].keys():
                bot.memory["botdict"]["tempvals"]['channels_list'][str(channel)] = dict()

            # all channels ever
            if str(channel) not in bot.memory["botdict"]['channels_list'].keys():
                bot.memory["botdict"]['channels_list'][str(channel)] = dict()

            # authorized user groups for channels
            if "auth_block" not in bot.memory["botdict"]['channels_list'][channel].keys():
                bot.memory["botdict"]['channels_list'][str(channel)]["auth_block"] = []
            if bot.memory["botdict"]['channels_list'][str(channel)]["auth_block"] == []:
                bot.memory["botdict"]['channels_list'][str(channel)]["auth_block"].append("all")

            # diabled commands per channel
            if "disabled_commands" not in bot.memory["botdict"]['channels_list'][channel].keys():
                bot.memory["botdict"]['channels_list'][str(channel)]["disabled_commands"] = {}


# other bot configs will be detected in this directory
def botdict_setup_bots(bot):

    if bot.memory["botdict"]["tempvals"]['bot_admins'] == []:
        bot.memory["botdict"]["tempvals"]['bot_admins'] = bot.config.core.admins
    if bot.memory["botdict"]["tempvals"]['bot_owners'] == []:
        bot.memory["botdict"]["tempvals"]['bot_owners'] = [bot.config.core.owner]

    if not bot.memory["botdict"]["tempvals"]['config_dir']:
        bot.memory["botdict"]["tempvals"]['config_dir'] = str("/home/spicebot/.sopel/" + bot.nick + "/System-Files/Configs/" + bot.memory["botdict"]["tempvals"]['servername'] + "/")

    # all bot configs present
    if bot.memory["botdict"]["tempvals"]['bots_list'].keys() == []:
        for filename in os.listdir(bot.memory["botdict"]["tempvals"]['config_dir']):
            filenameminuscfg = str(filename).replace(".cfg", "")
            if filenameminuscfg not in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
                bot.memory["botdict"]["tempvals"]['bots_list'][filenameminuscfg] = dict()

    for botconf in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
        if bot.memory["botdict"]["tempvals"]['bots_list'][botconf] == dict():
            if 'name' not in bot.memory["botdict"]["tempvals"]['bots_list'][botconf].keys():
                bot.memory["botdict"]["tempvals"]['bots_list'][botconf]['name'] = botconf
            if 'directory' not in bot.memory["botdict"]["tempvals"]['bots_list'][botconf].keys():
                joindpath = os.path.join("/home/spicebot/.sopel/", botconf)
                if os.path.isdir(joindpath):
                    bot.memory["botdict"]["tempvals"]['bots_list'][botconf]['directory'] = joindpath
                else:
                    bot.memory["botdict"]["tempvals"]['bots_list'][botconf]['directory'] = None
            if 'config_file' not in bot.memory["botdict"]["tempvals"]['bots_list'][botconf].keys():
                bot.memory["botdict"]["tempvals"]['config_file'] = str(bot.memory["botdict"]["tempvals"]['config_dir'] + str(botconf) + ".cfg")
            if 'configuration' not in bot.memory["botdict"]["tempvals"]['bots_list'][botconf].keys():
                bot.memory["botdict"]["tempvals"]['bots_list'][botconf]['configuration'] = dict()
                # Read configuration
                config = ConfigParser.ConfigParser()
                config.read(bot.memory["botdict"]["tempvals"]['config_file'])
                for each_section in config.sections():
                    if each_section not in bot.memory["botdict"]["tempvals"]['bots_list'][botconf]['configuration'].keys():
                        bot.memory["botdict"]["tempvals"]['bots_list'][botconf]['configuration'][each_section] = dict()
                        for (each_key, each_val) in config.items(each_section):
                            if each_key not in bot.memory["botdict"]["tempvals"]['bots_list'][botconf]['configuration'][each_section].keys():
                                bot.memory["botdict"]["tempvals"]['bots_list'][botconf]['configuration'][each_section][each_key] = each_val


# initial user list creation
def botdict_setup_users(bot):

    for channelcheck in bot.memory["botdict"]["tempvals"]['channels_list'].keys():

        if 'chanops' not in bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck].keys():
            bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck]['chanops'] = []

        if 'chanhalfops' not in bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck].keys():
            bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck]['chanhalfops'] = []

        if 'chanvoices' not in bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck].keys():
            bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck]['chanvoices'] = []

        if 'chanowners' not in bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck].keys():
            bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck]['chanowners'] = []

        if 'chanadmins' not in bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck].keys():
            bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck]['chanadmins'] = []

        if 'current_users' not in bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck].keys():
            bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck]['current_users'] = []

        userprivdict = dict()
        for user in bot.privileges[channelcheck].keys():
            if user not in bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck]['current_users'] and user not in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
                bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck]['current_users'].append(str(user))
            try:
                userprivdict[user] = bot.privileges[channelcheck][str(user)] or 0
            except KeyError:
                userprivdict[str(user)] = 0

        for user in userprivdict.keys():

            for privtype in ['VOICE', 'HALFOP', 'OP', 'ADMIN', 'OWNER']:
                privstring = str("chan" + privtype.lower() + "s")
                if userprivdict[user] == eval(privtype):
                    if user not in bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck][privstring]:
                        bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck][privstring].append(user)
                elif userprivdict[user] >= eval(privtype) and privtype == 'OWNER':
                    if user not in bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck][privstring]:
                        bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck][privstring].append(user)
                else:
                    if user in bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck][privstring]:
                        bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck][privstring].remove(user)

        for user in bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck]['current_users']:
            if user not in bot.memory["botdict"]["users"].keys():
                bot.memory["botdict"]["users"][user] = dict()
            if user not in bot.memory["botdict"]["tempvals"]['all_current_users']:
                bot.memory["botdict"]["tempvals"]['all_current_users'].append(user)

    for user in bot.memory["botdict"]["users"].keys():
        if user not in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
            if user not in bot.memory["botdict"]["tempvals"]['all_current_users']:
                if user not in bot.memory["botdict"]["tempvals"]['offline_users']:
                    bot.memory["botdict"]["tempvals"]['offline_users'].append(user)


# files in the txt files dir will be imported
def bot_read_txt_files(bot):
    # Don't load commands if already loaded
    if bot.memory["botdict"]["tempvals"]['txt_files'] != dict():
        return

    txt_file_path = bot.memory["botdict"]["tempvals"]['bots_list'][str(bot.nick)]['directory'] + "/Text-Files/"

    # iterate over files within
    for txtfile in os.listdir(txt_file_path):

        if txtfile != "ReadMe.MD":

            # check if text file is already in the list
            if txtfile not in bot.memory["botdict"]["tempvals"]['txt_files_loaded']:
                bot.memory["botdict"]["tempvals"]['txt_files_loaded'].append(txtfile)

            text_file_list = []
            text_file = open(os.path.join(txt_file_path, txtfile), 'r')
            lines = text_file.readlines()
            for line in lines:
                text_file_list.append(line)
            text_file.close()

            bot.memory["botdict"]["tempvals"]['txt_files'][txtfile] = text_file_list


# Command configs
def dict_command_configs(bot):

    # Don't load commands if already loaded
    if bot.memory["botdict"]["tempvals"]['dict_commands'] != dict():
        return

    quick_coms_path = bot.memory["botdict"]["tempvals"]['bots_list'][str(bot.nick)]['directory'] + "/Modules/Dictionary_replies/"

    # iterate over organizational folder
    dictcount, dictopenfail = 0, 0
    for quick_coms_type in os.listdir(quick_coms_path):

        # iterate over files within
        coms_type_file_path = os.path.join(quick_coms_path, quick_coms_type)
        for comconf in os.listdir(coms_type_file_path):

            # check if command file is already in the list
            if comconf not in bot.memory["botdict"]["tempvals"]['dict_commands_loaded']:
                bot.memory["botdict"]["tempvals"]['dict_commands_loaded'].append(comconf)

                # Read dictionary from file, if not, enable an empty dict
                filereadgood = True
                inf = codecs.open(os.path.join(coms_type_file_path, comconf), "r", encoding='utf-8')
                infread = inf.read()
                try:
                    dict_from_file = eval(infread)
                except Exception as e:
                    filereadgood = False
                    stderr("Error loading dict %s: %s (%s)" % (comconf, e, os.path.join(coms_type_file_path, comconf)))
                    dict_from_file = dict()
                # Close File
                inf.close()

                if filereadgood and isinstance(dict_from_file, dict):

                    dictcount += 1

                    # current file path
                    if "filepath" not in dict_from_file.keys():
                        dict_from_file["filepath"] = os.path.join(coms_type_file_path, comconf)

                    # default command to filename
                    if "validcoms" not in dict_from_file.keys():
                        dict_from_file["validcoms"] = [comconf]
                    elif dict_from_file["validcoms"] == []:
                        dict_from_file["validcoms"] = [comconf]
                    elif not isinstance(dict_from_file['validcoms'], list):
                        dict_from_file["validcoms"] = [dict_from_file["validcoms"]]

                    maincom = dict_from_file["validcoms"][0]
                    if len(dict_from_file["validcoms"]) > 1:
                        comaliases = spicemanip(bot, dict_from_file["validcoms"], '2+', 'list')
                    else:
                        comaliases = []

                    # check for tuple dict keys and split
                    for validkey in dict_from_file.keys():
                        if isinstance(validkey, tuple):
                            tuple_bak = validkey
                            tuple_contents_bak = dict_from_file[validkey]
                            del dict_from_file[validkey]
                            for var in tuple_bak:
                                dict_from_file[var] = tuple_contents_bak

                    if maincom not in bot.memory["botdict"]["tempvals"]['dict_commands'].keys():

                        # check that type is set, use cases will inherit this if not set
                        if "type" not in dict_from_file.keys():
                            dict_from_file["type"] = quick_coms_type.lower()
                        if dict_from_file["type"] not in valid_com_types:
                            dict_from_file["type"] = 'simple'

                        # Don't process these.
                        keysprocessed = []
                        keysprocessed.extend(["validcoms", "filepath"])

                        # the command must have an author
                        if "author" not in dict_from_file.keys():
                            dict_from_file["author"] = "deathbybandaid"
                        keysprocessed.append("author")

                        # the command must have a contributors list
                        if "contributors" not in dict_from_file.keys():
                            dict_from_file["contributors"] = []
                        if not isinstance(dict_from_file["contributors"], list):
                            dict_from_file["contributors"] = [dict_from_file["contributors"]]
                        if "deathbybandaid" not in dict_from_file["contributors"]:
                            dict_from_file["contributors"].append("deathbybandaid")
                        if dict_from_file["author"] not in dict_from_file["contributors"]:
                            dict_from_file["contributors"].append(dict_from_file["author"])
                        keysprocessed.append("contributors")

                        if "hardcoded_channel_block" not in dict_from_file.keys():
                            dict_from_file["hardcoded_channel_block"] = []
                        keysprocessed.append("hardcoded_channel_block")

                        # handle basic required dict handling
                        dict_required = ["?default"]
                        dict_from_file = bot_dict_use_cases(bot, maincom, dict_from_file, dict_required)
                        keysprocessed.extend(dict_required)

                        # remove later
                        keysprocessed.append("type")

                        # all other keys not processed above are considered potential use cases
                        otherkeys = []
                        for otherkey in dict_from_file.keys():
                            if otherkey not in keysprocessed:
                                otherkeys.append(otherkey)
                        if otherkeys != []:
                            dict_from_file = bot_dict_use_cases(bot, maincom, dict_from_file, otherkeys)
                        keysprocessed.extend(otherkeys)

                        bot.memory["botdict"]["tempvals"]['dict_commands'][maincom] = dict_from_file
                        for comalias in comaliases:
                            if comalias not in bot.memory["botdict"]["tempvals"]['dict_commands'].keys():
                                bot.memory["botdict"]["tempvals"]['dict_commands'][comalias] = {"aliasfor": maincom}
                else:
                    dictopenfail += 1
    if dictcount > 1:
        stderr('\n\nRegistered %d  dict files,' % (dictcount))
        stderr('%d dict files failed to load\n\n' % dictopenfail)
    else:
        stderr("Warning: Couldn't load any dict files")

    bot.memory["botdict"]["tempvals"]['dict_module_count'] = dictcount


# goes with the above function, is used for iteration over use cases
def bot_dict_use_cases(bot, maincom, dict_from_file, process_list):

    for mustbe in process_list:

        # All of the above need to be in the dict if not
        if mustbe not in dict_from_file.keys():
            dict_from_file[mustbe] = dict()

        # verify if already there, that the key is a dict
        if not isinstance(dict_from_file[mustbe], dict):
            dict_from_file[mustbe] = dict()

        # Each usecase for the command must have a type, flat files inherit this type
        if "type" not in dict_from_file[mustbe].keys():
            if "type" in dict_from_file.keys():
                dict_from_file[mustbe]["type"] = dict_from_file["type"]
            else:
                dict_from_file[mustbe]["type"] = "simple"

        # each usecase needs to know if it can be updated. Default is false
        if "updates_enabled" not in dict_from_file[mustbe].keys():
            dict_from_file[mustbe]["updates_enabled"] = False
        if dict_from_file[mustbe]["updates_enabled"]:
            if dict_from_file[mustbe]["updates_enabled"] not in ["shared", "user"]:
                dict_from_file[mustbe]["updates_enabled"] = "shared"

        # each usecase needs to know if it needs a target
        if "target_required" not in dict_from_file[mustbe].keys():
            if dict_from_file[mustbe]["type"] in ['target', 'targetplusreason']:
                dict_from_file[mustbe]["target_required"] = True
            else:
                dict_from_file[mustbe]["target_required"] = False
        if "target_backup" not in dict_from_file[mustbe].keys():
            dict_from_file[mustbe]["target_backup"] = False
        if "target_bypass" not in dict_from_file[mustbe].keys():
            dict_from_file[mustbe]["target_bypass"] = []

        # special target reactions
        for reason in ['self', 'bot', 'bots', 'offline', 'unknown', 'privmsg', 'diffchannel']:
            if 'react_'+reason not in dict_from_file[mustbe].keys():
                dict_from_file[mustbe]['react_'+reason] = False

        # each usecase needs to know if it needs input for fillintheblank
        if "blank_required" not in dict_from_file[mustbe].keys():
            if dict_from_file[mustbe]["type"] in ['fillintheblank', 'targetplusreason', "translate"]:
                dict_from_file[mustbe]["blank_required"] = True
            else:
                dict_from_file[mustbe]["blank_required"] = False
        if "blank_backup" not in dict_from_file[mustbe].keys():
            dict_from_file[mustbe]["blank_backup"] = False
        if "blank_fail" not in dict_from_file[mustbe].keys():
            dict_from_file[mustbe]["blank_fail"] = ["This command requires input."]
        if not isinstance(dict_from_file[mustbe]["blank_fail"], list):
            dict_from_file[mustbe]["blank_fail"] = [dict_from_file[mustbe]["blank_fail"]]

        if "blank_phrasehandle" not in dict_from_file[mustbe].keys():
            dict_from_file[mustbe]["blank_phrasehandle"] = False
        if dict_from_file[mustbe]["blank_phrasehandle"]:
            if not isinstance(dict_from_file[mustbe]["blank_phrasehandle"], list):
                dict_from_file[mustbe]["blank_phrasehandle"] = [dict_from_file[mustbe]["blank_phrasehandle"]]

        if "response_fail" not in dict_from_file[mustbe].keys():
            dict_from_file[mustbe]["response_fail"] = False
        if dict_from_file[mustbe]["response_fail"]:
            if not isinstance(dict_from_file[mustbe]["response_fail"], list):
                dict_from_file[mustbe]["response_fail"] = [dict_from_file[mustbe]["response_fail"]]

        if dict_from_file[mustbe]["updates_enabled"]:
            adjust_nick_array(bot, str(bot.nick), maincom + "_" + str(mustbe), dict_from_file[mustbe]["responses"], 'startup', 'long', 'sayings')
            dict_from_file[mustbe]["responses"] = get_nick_value(bot, str(bot.nick), maincom + "_" + str(mustbe), 'long', 'sayings') or []

        # each usecase needs a response
        if "responses" not in dict_from_file[mustbe].keys():
            dict_from_file[mustbe]["responses"] = []

        # verify responses are in list form
        if not isinstance(dict_from_file[mustbe]["responses"], list):
            if dict_from_file[mustbe]["responses"] in bot.memory["botdict"]["tempvals"]['txt_files'].keys():
                dict_from_file[mustbe]["responses"] = bot.memory["botdict"]["tempvals"]['txt_files'][dict_from_file[mustbe]["responses"]]
            elif str(dict_from_file[mustbe]["responses"]).startswith(tuple(["https://", "http://"])):
                page = requests.get(dict_from_file[mustbe]["responses"], headers=header)
                tree = html.fromstring(page.content)
                if page.status_code == 200:
                    htmlfile = urllib.urlopen(dict_from_file[mustbe]["responses"])
                    lines = htmlfile.read().splitlines()
                    dict_from_file[mustbe]["responses"] = lines
            else:
                dict_from_file[mustbe]["responses"] = [dict_from_file[mustbe]["responses"]]

        # each usecase needs a prefixtext
        if "prefixtext" not in dict_from_file[mustbe].keys():
            dict_from_file[mustbe]["prefixtext"] = False
        if dict_from_file[mustbe]["prefixtext"]:
            if not isinstance(dict_from_file[mustbe]["prefixtext"], list):
                dict_from_file[mustbe]["prefixtext"] = [dict_from_file[mustbe]["prefixtext"]]

        # each usecase needs a suffixtext
        if "suffixtext" not in dict_from_file[mustbe].keys():
            dict_from_file[mustbe]["suffixtext"] = False
        if dict_from_file[mustbe]["suffixtext"]:
            if not isinstance(dict_from_file[mustbe]["suffixtext"], list):
                dict_from_file[mustbe]["suffixtext"] = [dict_from_file[mustbe]["suffixtext"]]

        # Translations
        if "translations" not in dict_from_file[mustbe].keys():
            dict_from_file[mustbe]["translations"] = False
        if dict_from_file[mustbe]["translations"]:
            if not isinstance(dict_from_file[mustbe]["translations"], list):
                dict_from_file[mustbe]["translations"] = [dict_from_file[mustbe]["translations"]]

        # make sure we have the smaller variation list
        if "replyvariation" not in dict_from_file[mustbe].keys():
            dict_from_file[mustbe]["replyvariation"] = []
        if not isinstance(dict_from_file[mustbe]["replyvariation"], list):
            dict_from_file[mustbe]["replyvariation"] = [dict_from_file[mustbe]["replyvariation"]]

        # This is to provide functionality for flat dictionaries responses
        if dict_from_file[mustbe]["responses"] == [] and mustbe == "?default":
            if "responses" in dict_from_file.keys():
                if isinstance(dict_from_file["responses"], list):
                    dict_from_file[mustbe]["responses"].extend(dict_from_file["responses"])
                else:
                    dict_from_file[mustbe]["responses"].append(dict_from_file["responses"])
                del dict_from_file["responses"]

        # Verify responses list is not empty
        if dict_from_file[mustbe]["responses"] == []:
            dict_from_file[mustbe]["responses"].append("No " + str(mustbe) + " responses set for " + str(maincom) + ".")

        # Some commands run query mode
        if "search_fail" not in dict_from_file[mustbe].keys():
            dict_from_file[mustbe]["search_fail"] = None
        if dict_from_file[mustbe]["search_fail"]:
            if not isinstance(dict_from_file[mustbe]["search_fail"], list):
                dict_from_file[mustbe]["search_fail"] = [dict_from_file[mustbe]["search_fail"]]

        if "selection_allowed" not in dict_from_file[mustbe].keys():
            dict_from_file[mustbe]["selection_allowed"] = True

        # Translations
        if "randnum" not in dict_from_file[mustbe].keys():
            dict_from_file[mustbe]["randnum"] = False
        if dict_from_file[mustbe]["randnum"]:
            if not isinstance(dict_from_file[mustbe]["randnum"], list):
                dict_from_file[mustbe]["randnum"] = [0, 50]
            if len(dict_from_file[mustbe]["randnum"]) == 1:
                dict_from_file[mustbe]["randnum"] = [0, dict_from_file[mustbe]["randnum"][0]]

        if "hardcoded_channel_block" not in dict_from_file[mustbe].keys():
            dict_from_file[mustbe]["hardcoded_channel_block"] = []

    return dict_from_file


# startup privacy sweep
def bot_setup_privacy_sweep(bot):
    for channelcheck in bot.memory["botdict"]['channels_list'].keys():
        allowedusers = []
        if "all" not in bot.memory["botdict"]['channels_list'][channelcheck]['auth_block'] and bot.privileges[channelcheck.lower()][bot.nick.lower()] >= module.OP:
            bot.msg(channelcheck, "Running User Sweep for " + channelcheck + ". Unauthorized users will be kicked.")
            for authedgroup in bot.memory["botdict"]['channels_list'][channelcheck]['auth_block']:
                if authedgroup == 'OP':
                    allowedusers.extend(bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck]['chanops'])
                elif authedgroup == 'HOP':
                    allowedusers.extend(bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck]['chanhalfops'])
                elif authedgroup == 'VOICE':
                    allowedusers.extend(bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck]['chanvoices'])
                elif authedgroup == 'OWNER':
                    allowedusers.extend(bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck]['chanowners'])
                elif authedgroup == 'ADMIN':
                    allowedusers.extend(bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck]['chanadmins'])
                elif authedgroup == 'admin':
                    allowedusers.extend(bot.memory["botdict"]["tempvals"]['bot_admins'])
                elif authedgroup == 'owner':
                    allowedusers.extend(bot.memory["botdict"]["tempvals"]['bot_owners'])
            kickinglist = []
            for user in bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck]['current_users']:
                if user not in allowedusers:
                    kickinglist.append(user)
            for user in kickinglist:
                bot.write(['KICK', channelcheck, user], "You are not authorized to join " + channelcheck + ".")


# This is how the dict is saved to the database
def botdict_save(bot):
    botdict_open(bot)

    # copy dict to not overwrite
    savedict = bot.memory["botdict"].copy()

    # Values to not save to database
    savedict_del = ['tempvals', 'static']
    for dontsave in savedict_del:
        if dontsave in savedict.keys():
            del savedict[dontsave]

    # save to database
    set_database_value(bot, bot.nick, 'bot_dict', savedict)


"""
Trigger watching
"""


# handling for commands run from the bot's nick
def bot_nickcom_run(bot, trigger):

    # botcom dynamic Class
    botcom = class_create('botcom')
    botcom.default = 'botcom'

    # instigator
    botcom.instigator = str(trigger.nick)

    # channel
    botcom.channel_current = str(trigger.sender)

    # Bots can't run commands
    if botcom.instigator in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
        return

    # valid commands
    global valid_botnick_commands

    # create arg list
    botcom.triggerargsarray = spicemanip(bot, trigger, '2+', 'list')

    # IF "&&" is in the full input, it is treated as multiple commands, and is split
    commands_array = spicemanip(bot, botcom.triggerargsarray, "split_&&")
    if commands_array == []:
        commands_array = [[]]
    invalidcomslist = []
    for command_split_partial in commands_array:
        botcom.triggerargsarray = spicemanip(bot, command_split_partial, 'create')

        # Command Used
        botcom.command_main = spicemanip(bot, botcom.triggerargsarray, 1)
        botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+', 'list')

        if botcom.command_main.lower() in valid_botnick_commands.keys():

            if bot_nickcom_run_check(bot, botcom):

                bot_nickcom_function_run = str('bot_nickcom_function_' + botcom.command_main.lower() + '(bot, botcom)')
                eval(bot_nickcom_function_run)
            else:
                invalidcomslist.append(botcom.command_main)

    # Display Invalids coms used
    if invalidcomslist != []:
        osd(bot, botcom.instigator, 'notice', "I was unable to process the following Bot Nick commands due to privilege issues: " + spicemanip(bot, invalidcomslist, 'andlist'))

    # save dictionary now
    botdict_save(bot)


# most of these nick commands require privilege to run
def bot_nickcom_run_check(bot, botcom):
    global valid_botnick_commands
    commandrun = True

    if 'privs' in valid_botnick_commands[botcom.command_main.lower()].keys():
        commandrunconsensus = []

        if 'admin' in valid_botnick_commands[botcom.command_main.lower()]['privs']:
            if botcom.instigator not in bot.memory["botdict"]["tempvals"]['bot_admins']:
                commandrunconsensus.append('False')
            else:
                commandrunconsensus.append('True')

        if 'OP' in valid_botnick_commands[botcom.command_main.lower()]['privs']:
            if botcom.channel_current.startswith('#'):
                if botcom.instigator not in bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['chanops']:
                    commandrunconsensus.append('False')
                else:
                    commandrunconsensus.append('True')
            else:
                commandrunconsensus.append('False')

        if 'HOP' in valid_botnick_commands[botcom.command_main.lower()]['privs']:
            if botcom.channel_current.startswith('#'):
                if botcom.instigator not in bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['chanhalfops']:
                    commandrunconsensus.append('False')
                else:
                    commandrunconsensus.append('True')
            else:
                commandrunconsensus.append('False')

        if 'VOICE' in valid_botnick_commands[botcom.command_main.lower()]['privs']:
            if botcom.channel_current.startswith('#'):
                if botcom.instigator not in bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['chanvoices']:
                    commandrunconsensus.append('False')
                else:
                    commandrunconsensus.append('True')
            else:
                commandrunconsensus.append('False')

        if 'OWNER' in valid_botnick_commands[botcom.command_main.lower()]['privs']:
            if botcom.channel_current.startswith('#'):
                if botcom.instigator not in bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['chanowners']:
                    commandrunconsensus.append('False')
                else:
                    commandrunconsensus.append('True')
            else:
                commandrunconsensus.append('False')

        if 'ADMIN' in valid_botnick_commands[botcom.command_main.lower()]['privs']:
            if botcom.channel_current.startswith('#'):
                if botcom.instigator not in bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['chanadmins']:
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


# how we handdle user PART
def bot_watch_part_run(bot, trigger):

    # botcom dynamic Class
    botcom = class_create('botcom')
    botcom.default = 'botcom'

    # instigator
    botcom.instigator = str(trigger.nick)

    # channel
    botcom.channel_current = str(trigger.sender)

    # database entry for user
    if botcom.instigator not in bot.memory["botdict"]["users"].keys():
        bot.memory["botdict"]["users"][botcom.instigator] = dict()

    # channel list
    if botcom.instigator in bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['current_users']:
        bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['current_users'].remove(botcom.instigator)

    # status
    for status in ['chanops', 'chanhalfops', 'chanvoices', 'chanowners', 'chanadmins', 'current_users']:
        if botcom.instigator in bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current][status]:
            bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current][status].remove(botcom.instigator)

    online = False
    onlineconsensus = []
    for channel in bot.memory["botdict"]["tempvals"]['channels_list'].keys():
        if botcom.instigator in bot.memory["botdict"]["tempvals"]['channels_list'][channel]['current_users']:
            onlineconsensus.append("True")
        else:
            onlineconsensus.append("False")

    if 'True' not in onlineconsensus:
        online = False

    if not online:

        if botcom.instigator not in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
            if botcom.instigator not in bot.memory["botdict"]["tempvals"]['offline_users']:
                bot.memory["botdict"]["tempvals"]['offline_users'].append(botcom.instigator)

        if botcom.instigator in bot.memory["botdict"]["tempvals"]['all_current_users']:
            bot.memory["botdict"]["tempvals"]['all_current_users'].remove(botcom.instigator)


# how we handdle user KICK
def bot_watch_kick_run(bot, trigger):

    # botcom dynamic Class
    botcom = class_create('botcom')
    botcom.default = 'botcom'

    # instigator
    botcom.instigator = str(trigger.nick)

    # channel
    botcom.channel_current = str(trigger.sender)

    # target user
    botcom.target = str(trigger.args[1])

    # database entry for user
    if botcom.target not in bot.memory["botdict"]["users"].keys():
        bot.memory["botdict"]["users"][botcom.target] = dict()

    # channel list
    if botcom.target in bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['current_users']:
        bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['current_users'].remove(botcom.target)

    # status
    for status in ['chanops', 'chanhalfops', 'chanvoices', 'chanowners', 'chanadmins', 'current_users']:
        if botcom.target in bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current][status]:
            bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current][status].remove(botcom.target)

    online = False
    onlineconsensus = []
    for channel in bot.memory["botdict"]["tempvals"]['channels_list'].keys():
        if botcom.instigator in bot.memory["botdict"]["tempvals"]['channels_list'][channel]['current_users']:
            onlineconsensus.append("True")
        else:
            onlineconsensus.append("False")

    if 'True' not in onlineconsensus:
        online = False

    if not online:

        if botcom.instigator not in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
            if botcom.instigator not in bot.memory["botdict"]["tempvals"]['offline_users']:
                bot.memory["botdict"]["tempvals"]['offline_users'].append(botcom.instigator)

        if botcom.instigator in bot.memory["botdict"]["tempvals"]['all_current_users']:
            bot.memory["botdict"]["tempvals"]['all_current_users'].remove(botcom.instigator)


# watch nick changing
def bot_watch_nick_run(bot, trigger):

    # botcom dynamic Class
    botcom = class_create('botcom')
    botcom.default = 'botcom'

    # instigator
    botcom.instigator = str(trigger.nick)

    # channel
    botcom.channel_current = str(trigger.sender)

    botcom.target = str(trigger.args[0])

    # database entry for user
    if botcom.instigator not in bot.memory["botdict"]["users"].keys():
        bot.memory["botdict"]["users"][botcom.instigator] = dict()
    if botcom.target not in bot.memory["botdict"]["users"].keys():
        bot.memory["botdict"]["users"][botcom.target] = dict()

    # channel list
    for channel in bot.memory["botdict"]["tempvals"]['channels_list'].keys():
        if botcom.instigator in bot.memory["botdict"]["tempvals"]['channels_list'][channel]['current_users']:
            bot.memory["botdict"]["tempvals"]['channels_list'][channel]['current_users'].remove(botcom.instigator)
            if botcom.target not in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
                bot.memory["botdict"]["tempvals"]['channels_list'][channel]['current_users'].append(botcom.target)

        # status
        for status in ['chanops', 'chanhalfops', 'chanvoices', 'chanowners', 'chanadmins', 'current_users']:
            if botcom.instigator in bot.memory["botdict"]["tempvals"]['channels_list'][channel][status]:
                bot.memory["botdict"]["tempvals"]['channels_list'][channel][status].remove(botcom.instigator)
        if botcom.target in bot.privileges[channel].keys():
            userprivdict = dict()
            try:
                userprivdict[botcom.target] = bot.privileges[channel][botcom.target] or 0
            except KeyError:
                userprivdict[botcom.target] = 0
            for privtype in ['VOICE', 'HALFOP', 'OP', 'ADMIN', 'OWNER']:
                privstring = str("chan" + privtype.lower() + "s")
                if userprivdict[botcom.target] == eval(privtype):
                    if botcom.target not in bot.memory["botdict"]["tempvals"]['channels_list'][channel][privstring]:
                        bot.memory["botdict"]["tempvals"]['channels_list'][channel][privstring].append(botcom.target)
                elif userprivdict[botcom.target] >= eval(privtype) and privtype == 'OWNER':
                    if botcom.target not in bot.memory["botdict"]["tempvals"]['channels_list'][channel][privstring]:
                        bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck][privstring].append(botcom.target)
                else:
                    if botcom.target in bot.memory["botdict"]["tempvals"]['channels_list'][channel][privstring]:
                        bot.memory["botdict"]["tempvals"]['channels_list'][channel][privstring].remove(botcom.target)

    # offline
    if botcom.instigator not in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
        if botcom.instigator not in bot.memory["botdict"]["tempvals"]['offline_users']:
            bot.memory["botdict"]["tempvals"]['offline_users'].append(botcom.instigator)
    if botcom.target in bot.memory["botdict"]["tempvals"]['offline_users']:
        bot.memory["botdict"]["tempvals"]['offline_users'].remove(botcom.target)

    # all current users
    if botcom.instigator in bot.memory["botdict"]["tempvals"]['all_current_users']:
        bot.memory["botdict"]["tempvals"]['all_current_users'].remove(botcom.instigator)
    if botcom.target not in bot.memory["botdict"]["tempvals"]['all_current_users']:
        bot.memory["botdict"]["tempvals"]['all_current_users'].append(botcom.target)


# how we handdle user QUIT
def bot_watch_quit_run(bot, trigger):

    # botcom dynamic Class
    botcom = class_create('botcom')
    botcom.default = 'botcom'

    # instigator
    botcom.instigator = str(trigger.nick)

    # channel
    botcom.channel_current = str(trigger.sender)

    # database entry for user
    if botcom.instigator not in bot.memory["botdict"]["users"].keys():
        bot.memory["botdict"]["users"][botcom.instigator] = dict()

    # channel list
    for channel in bot.memory["botdict"]["tempvals"]['channels_list'].keys():
        if botcom.instigator in bot.memory["botdict"]["tempvals"]['channels_list'][channel]['current_users']:
            bot.memory["botdict"]["tempvals"]['channels_list'][channel]['current_users'].remove(botcom.instigator)

        # status
        for status in ['chanops', 'chanhalfops', 'chanvoices', 'chanowners', 'chanadmins', 'current_users']:
            if botcom.instigator in bot.memory["botdict"]["tempvals"]['channels_list'][channel][status]:
                bot.memory["botdict"]["tempvals"]['channels_list'][channel][status].remove(botcom.instigator)

    if botcom.instigator not in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
        if botcom.instigator not in bot.memory["botdict"]["tempvals"]['offline_users']:
            bot.memory["botdict"]["tempvals"]['offline_users'].append(botcom.instigator)

    if botcom.instigator in bot.memory["botdict"]["tempvals"]['all_current_users']:
        bot.memory["botdict"]["tempvals"]['all_current_users'].remove(botcom.instigator)


# how we handdle user JOIN
def bot_watch_join_run(bot, trigger):

    # botcom dynamic Class
    botcom = class_create('botcom')
    botcom.default = 'botcom'

    # instigator
    botcom.instigator = str(trigger.nick)

    # channel
    botcom.channel_current = str(trigger.sender)

    # Privacy Sweep
    allowedusers = []
    if "all" not in bot.memory["botdict"]['channels_list'][botcom.channel_current]['auth_block'] and bot.privileges[botcom.channel_current.lower()][bot.nick.lower()] >= module.OP:
        # give chanserv time to OP
        time.sleep(5)
        for authedgroup in bot.memory["botdict"]['channels_list'][botcom.channel_current]['auth_block']:
            if authedgroup == 'OP':
                allowedusers.extend(bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['chanops'])
            elif authedgroup == 'HOP':
                allowedusers.extend(bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['chanhalfops'])
            elif authedgroup == 'VOICE':
                allowedusers.extend(bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['chanvoices'])
            elif authedgroup == 'OWNER':
                allowedusers.extend(bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['chanowners'])
            elif authedgroup == 'ADMIN':
                allowedusers.extend(bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['chanadmins'])
            elif authedgroup == 'admin':
                allowedusers.extend(bot.memory["botdict"]["tempvals"]['bot_admins'])
            elif authedgroup == 'owner':
                allowedusers.extend(bot.memory["botdict"]["tempvals"]['bot_owners'])
        if botcom.instigator not in allowedusers:
            bot.write(['KICK', botcom.channel_current, botcom.instigator], "You are not authorized to join " + botcom.channel_current + ".")
            return

    # database entry for user
    if botcom.instigator not in bot.memory["botdict"]["users"].keys():
        bot.memory["botdict"]["users"][botcom.instigator] = dict()

    if botcom.instigator not in bot.memory["botdict"]["tempvals"]['bots_list'].keys():

        # channel list
        if botcom.instigator not in bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['current_users']:
            bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['current_users'].append(botcom.instigator)

        # all current users and offline users
        if botcom.instigator not in bot.memory["botdict"]["tempvals"]['all_current_users']:
            bot.memory["botdict"]["tempvals"]['all_current_users'].append(botcom.instigator)

    userprivdict = dict()
    try:
        userprivdict[botcom.instigator] = bot.privileges[botcom.channel_current][botcom.instigator] or 0
    except KeyError:
        userprivdict[botcom.instigator] = 0
    for privtype in ['VOICE', 'HALFOP', 'OP', 'ADMIN', 'OWNER']:
        privstring = str("chan" + privtype.lower() + "s")
        if userprivdict[botcom.instigator] == eval(privtype):
            if botcom.instigator not in bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current][privstring]:
                bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current][privstring].append(botcom.instigator)
        elif userprivdict[botcom.instigator] >= eval(privtype) and privtype == 'OWNER':
            if botcom.instigator not in bot.memory["botdict"]["tempvals"]['channels_list'][channel][privstring]:
                bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck][privstring].append(botcom.instigator)
        else:
            if botcom.instigator in bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current][privstring]:
                bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current][privstring].remove(botcom.instigator)

    # remove from offline
    if botcom.instigator in bot.memory["botdict"]["tempvals"]['offline_users']:
        bot.memory["botdict"]["tempvals"]['offline_users'].remove(botcom.instigator)


# how we handdle user and channel MODE
def bot_watch_mode_run(bot, trigger):

    global mode_dict_alias

    # botcom dynamic Class
    botcom = class_create('botcom')
    botcom.default = 'botcom'

    # instigator
    botcom.instigator = str(trigger.nick)

    # channel
    botcom.channel_current = str(trigger.sender)

    # target
    target = str(trigger.args[-1])

    # Mode set
    modeused = str(trigger.args[1])

    if str(modeused).startswith("-"):
        modetype = 'del'
    elif str(modeused).startswith("+"):
        modetype = 'add'

    if modeused[1:] in mode_dict_alias.keys():

        userprivdict = dict()
        userprivdict[target] = eval(mode_dict_alias[modeused[1:]])

        for privtype in ['VOICE', 'HALFOP', 'OP', 'ADMIN', 'OWNER']:
            privstring = str("chan" + privtype.lower() + "s")
            if modetype == 'add':
                if userprivdict[target] == eval(privtype):
                    if target not in bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current][privstring]:
                        bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current][privstring].append(target)
                else:
                    if target in bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current][privstring]:
                        bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current][privstring].remove(target)
            elif modetype == 'del':
                if userprivdict[target] == eval(privtype):
                    if target in bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current][privstring]:
                        bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current][privstring].remove(target)
                else:
                    if target in bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current][privstring]:
                        bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current][privstring].remove(target)

        # Privacy Sweep
        allowedusers = []
        if "all" not in bot.memory["botdict"]['channels_list'][botcom.channel_current]['auth_block'] and bot.privileges[botcom.channel_current.lower()][bot.nick.lower()] >= module.OP:
            for authedgroup in bot.memory["botdict"]['channels_list'][botcom.channel_current]['auth_block']:
                if authedgroup == 'OP':
                    allowedusers.extend(bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['chanops'])
                elif authedgroup == 'HOP':
                    allowedusers.extend(bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['chanhalfops'])
                elif authedgroup == 'VOICE':
                    allowedusers.extend(bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['chanvoices'])
                elif authedgroup == 'OWNER':
                    allowedusers.extend(bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['chanowners'])
                elif authedgroup == 'ADMIN':
                    allowedusers.extend(bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['chanadmins'])
                elif authedgroup == 'admin':
                    allowedusers.extend(bot.memory["botdict"]["tempvals"]['bot_admins'])
                elif authedgroup == 'owner':
                    allowedusers.extend(bot.memory["botdict"]["tempvals"]['bot_owners'])
            if target not in allowedusers:
                bot.write(['KICK', botcom.channel_current, target], "You are not authorized to join " + botcom.channel_current + ".")
                return


# the query command watches everytime a ? is use
def bot_dictquery_run(bot, trigger):

    if not str(trigger).startswith(tuple(['?'])):
        return

    # botcom dynamic Class
    botcom = class_create('botcom')
    botcom.default = 'botcom'

    # instigator
    botcom.instigator = trigger.nick

    # channel
    botcom.channel_current = trigger.sender

    # Bots can't run commands
    if botcom.instigator in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
        return

    # create arg list
    botcom.triggerargsarray = spicemanip(bot, trigger, 'create')

    # command issued, check if valid
    botcom.querycommand = spicemanip(bot, botcom.triggerargsarray, 1).lower()[1:]
    if len(botcom.querycommand) == 1:
        commandlist = []
        for command in bot.memory["botdict"]["tempvals"]['dict_commands'].keys():
            if command.lower().startswith(botcom.querycommand):
                commandlist.append(command)
        if commandlist == []:
            return osd(bot, botcom.instigator, 'say', "No commands match " + str(botcom.querycommand) + ".")
        else:
            return osd(bot, botcom.instigator, 'say', "The following commands match " + str(botcom.querycommand) + ": " + spicemanip(bot, commandlist, 'andlist') + ".")

    elif botcom.querycommand.endswith(tuple(["+"])):
        botcom.querycommand = botcom.querycommand[:-1]
        if botcom.querycommand not in bot.memory["botdict"]["tempvals"]['dict_commands'].keys():
            return osd(bot, botcom.instigator, 'say', "The " + str(botcom.querycommand) + " does not appear to be valid.")
        realcom = botcom.querycommand
        if "aliasfor" in bot.memory["botdict"]["tempvals"]['dict_commands'][botcom.querycommand].keys():
            realcom = bot.memory["botdict"]["tempvals"]['dict_commands'][botcom.querycommand]["aliasfor"]
        validcomlist = bot.memory["botdict"]["tempvals"]['dict_commands'][realcom]["validcoms"]
        return osd(bot, botcom.instigator, 'say', "The following commands match " + str(botcom.querycommand) + ": " + spicemanip(bot, validcomlist, 'andlist') + ".")

    elif botcom.querycommand.endswith(tuple(['?'])):
        botcom.querycommand = botcom.querycommand[:-1]
        sim_com, sim_num = [], []
        for com in bot.memory['botdict']['tempvals']['dict_commands'].keys():
            similarlevel = similar(botcom.querycommand.lower(), com.lower())
            sim_com.append(com)
            sim_num.append(similarlevel)
        sim_num, sim_com = array_arrangesort(bot, sim_num, sim_com)
        closestmatch = spicemanip(bot, sim_com, 'reverse', "list")
        listnumb, relist = 1, []
        for item in closestmatch:
            if listnumb <= 10:
                relist.append(str(item))
            listnumb += 1
        return osd(bot, botcom.instigator, 'say', "The following commands may match " + str(botcom.querycommand) + ": " + spicemanip(bot, relist, 'andlist') + ".")

    elif botcom.querycommand in bot.memory["botdict"]["tempvals"]['dict_commands'].keys():
        return osd(bot, botcom.instigator, 'say', "The following commands match " + str(botcom.querycommand) + ": " + str(botcom.querycommand) + ".")

    elif not botcom.querycommand:
        return

    else:
        commandlist = []
        for command in bot.memory["botdict"]["tempvals"]['dict_commands'].keys():
            if command.lower().startswith(botcom.querycommand):
                commandlist.append(command)
        if commandlist == []:
            return osd(bot, botcom.instigator, 'say', "No commands match " + str(botcom.querycommand) + ".")
        else:
            return osd(bot, botcom.instigator, 'say', "The following commands match " + str(botcom.querycommand) + ": " + spicemanip(bot, commandlist, 'andlist') + ".")


# watches for dot commands
def bot_watch_dot_run(bot, trigger):

    if not str(trigger).startswith(tuple(['.'])):
        return

    # botcom dynamic Class
    botcom = class_create('botcom')
    botcom.default = 'botcom'

    # instigator
    botcom.instigator = trigger.nick

    # channel
    botcom.channel_current = trigger.sender

    # Bots can't run commands
    if botcom.instigator in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
        return

    # create arg list
    botcom.triggerargsarray = spicemanip(bot, trigger, 'create')

    # command issued, check if valid
    botcom.dotcommand = spicemanip(bot, botcom.triggerargsarray, 1).lower()[1:]
    if botcom.dotcommand in bot.memory["botdict"]["tempvals"]['dict_commands'].keys():
        bot_dictcom_handle(bot, botcom)

    # save dictionary now
    botdict_save(bot)


"""
Jobs Handling
"""


def bot_saved_jobs_process(bot, trigger, jobtype, timeset='asap'):

    if timeset == 'asap':
        timeset = time.time()

    # ID #
    dictsave = {"jobtype": jobtype, "trigger": trigger, "timeset": timeset}

    if "bot_jobs" not in bot.memory:
        bot.memory["bot_jobs"] = []

    id_numbs = [0]
    for botjob_dict in bot.memory["bot_jobs"]:
        id_numbs.append(int(botjob_dict["ID"]))
    highest_id = max(id_numbs)
    dictsave["ID"] = int(highest_id + 1)

    bot.memory["bot_jobs"].append(dictsave)


def bot_saved_jobs_run(bot):

    now = now = time.time()

    if "bot_jobs" not in bot.memory:
        bot.memory["bot_jobs"] = []

    ids_run = []
    for botjob_dict in bot.memory["bot_jobs"]:
        if now >= botjob_dict["timeset"]:
            trigger = botjob_dict["trigger"]
            jobeval = str(botjob_dict["jobtype"] + '_run(bot, trigger)')
            eval(jobeval)
            ids_run.append(int(botjob_dict["ID"]))

    for botjob_dict in bot.memory["bot_jobs"]:
        if int(botjob_dict["ID"]) in ids_run:
            ids_run.remove(int(botjob_dict["ID"]))
            bot.memory["bot_jobs"].remove(botjob_dict)

    botdict_save(bot)


"""
Authorization in channels
"""


def bot_nickcom_function_sweep(bot, botcom):
    bot_setup_privacy_sweep(bot)


def bot_nickcom_function_auth(bot, botcom):

    # Channel
    targetchannels = []
    if botcom.triggerargsarray == []:
        if botcom.channel_current.startswith('#'):
            targetchannels.append(botcom.channel_current)
        else:
            osd(bot, botcom.instigator, 'notice', "You must specify a valid channel.")
            return
    else:
        for targetchan in botcom.triggerargsarray:
            if targetchan in bot.memory["botdict"]["tempvals"]['channels_list'].keys():
                targetchannels.append(targetchan)
    if targetchannels == []:
        return osd(bot, botcom.instigator, 'notice', "You must specify a valid channel.")

    directionchange = None
    for possdirection in botcom.triggerargsarray:
        if possdirection in ['add', 'del', 'view']:
            directionchange = possdirection
    if not directionchange:
        return osd(bot, botcom.instigator, 'notice', "You must specify a valid add/del.")
    elif directionchange == 'view':
        osdmessage = []
        for channelcheck in targetchannels:
            osdmessage.append(str(channelcheck) + " permitted users list is currently set to " + str(spicemanip(bot, bot.memory["botdict"]['channels_list'][channelcheck]['auth_block'], 'andlist')))
        return osd(bot, botcom.channel_current, 'say', osdmessage)

    # usergroup target (case sensative)
    targetgroups = []
    for targetgroup in botcom.triggerargsarray:
        if targetgroup in ['OP', 'HOP', 'VOICE', 'OWNER', 'ADMIN', 'admin', 'all']:
            targetgroups.append(targetgroup)
    if targetgroups == []:
        return osd(bot, botcom.instigator, 'notice', "You must specify a valid targetgroup.")

    osdmessage = []
    for channelcheck in targetchannels:
        for groups in targetgroups:
            if directionchange == 'add':
                if groups not in bot.memory["botdict"]['channels_list'][channelcheck]['auth_block']:
                    bot.memory["botdict"]['channels_list'][channelcheck]['auth_block'].append(groups)
            elif directionchange == 'del':
                if groups in bot.memory["botdict"]['channels_list'][channelcheck]['auth_block']:
                    bot.memory["botdict"]['channels_list'][channelcheck]['auth_block'].remove(groups)
        if bot.memory["botdict"]['channels_list'][channelcheck]['auth_block'] == []:
            bot.memory["botdict"]['channels_list'][channelcheck]['auth_block'].append("all")
        osdmessage.append(str(channelcheck) + " permitted users list is now set to " + str(spicemanip(bot, bot.memory["botdict"]['channels_list'][channelcheck]['auth_block'], 'andlist')))
    return osd(bot, botcom.channel_current, 'say', osdmessage)

    bot_setup_privacy_sweep(bot)


"""
Basic Running Operations
"""


def bot_nickcom_function_update(bot, botcom):

    targetbots = []
    if botcom.triggerargsarray == []:
        targetbots.append(bot.nick)
    elif 'all' in botcom.triggerargsarray:
        for targetbot in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
            targetbots.append(targetbot)
    else:
        for targetbot in botcom.triggerargsarray:
            if targetbot in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
                targetbots.append(targetbot)

    # current bot should be last
    if str(bot.nick) in targetbots:
        targetbots.remove(str(bot.nick))
        targetbots.append(str(bot.nick))

    if targetbots == []:
        osd(bot, botcom.instigator, 'notice', "You have selected no bots to update.")
        return

    cannotproceed = []
    botcount = len(targetbots)

    if botcount == 1 and targetbots[0] == str(bot.nick):
        if targetbots[0] in bot.memory["botdict"]["static"]['bots']["update_text"].keys():
            osd(bot, botcom.channel_current, 'say', bot.memory["botdict"]["static"]['bots']["update_text"][targetbots[0]].replace("$instigator", botcom.instigator))
        else:
            osd(bot, botcom.channel_current, 'say', botcom.instigator + " commanded me to update from Github and restart. Be Back Soon!")
    else:
        osd(bot, [botcom.channel_current], 'say', botcom.instigator + " commanded me to update " + spicemanip(bot, targetbots, 'andlist') + " from Github and restart.")

    for targetbot in targetbots:

        if bot.memory["botdict"]["tempvals"]['bots_list'][targetbot]['directory']:

            osd(bot, botcom.channel_current, 'action', "Is Pulling " + str(bot.memory["botdict"]["tempvals"]['bots_list'][targetbot]['directory']) + " From Github...")
            bot_update(bot, targetbot)

            osd(bot, botcom.channel_current, 'action', "Is Restarting the " + targetbot + " Service...")
            bot_restart(bot, targetbot)

            if bot.nick == targetbot:
                osd(bot, botcom.channel_current, 'say', "If you see this, the service is hanging. Making another attempt.")
                bot_restart(bot, targetbot)

            botcount -= 1
            if botcount > 0:
                osd(bot, botcom.channel_current, 'say', "     ")

        else:
            cannotproceed.append(targetbot)

    if cannotproceed != []:
        osd(bot, botcom.channel_current, 'say', spicemanip(bot, cannotproceed, 'andlist') + " could not be updated.")


def bot_nickcom_function_restart(bot, botcom):

    targetbots = []
    if botcom.triggerargsarray == []:
        targetbots.append(bot.nick)
    elif 'all' in botcom.triggerargsarray:
        for targetbot in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
            targetbots.append(targetbot)
    else:
        for targetbot in botcom.triggerargsarray:
            if targetbot in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
                targetbots.append(targetbot)

    # current bot should be last
    if str(bot.nick) in targetbots:
        targetbots.remove(str(bot.nick))
        targetbots.append(str(bot.nick))

    if targetbots == []:
        osd(bot, botcom.instigator, 'notice', "You have selected no bots to restart.")
        return

    cannotproceed = []
    botcount = len(targetbots)
    if botcount == 1 and targetbots[0] == str(bot.nick):
        if targetbots[0] in bot.memory["botdict"]["static"]['bots']["restart_text"].keys():
            osd(bot, botcom.channel_current, 'say', bot.memory["botdict"]["static"]['bots']["restart_text"][targetbots[0]].replace("$instigator", botcom.instigator))
        else:
            osd(bot, botcom.channel_current, 'say', botcom.instigator + " commanded me to restart. Be Back Soon!")
    else:
        osd(bot, [botcom.channel_current], 'say', botcom.instigator + " commanded me to restart " + spicemanip(bot, targetbots, 'andlist'))

    for targetbot in targetbots:

        if bot.memory["botdict"]["tempvals"]['bots_list'][targetbot]['directory']:

            osd(bot, botcom.channel_current, 'action', "Is Restarting the " + targetbot + " Service...")
            bot_restart(bot, targetbot)

            if bot.nick == targetbot:
                osd(bot, botcom.channel_current, 'say', "If you see this, the service is hanging. Making another attempt.")
                bot_restart(bot, targetbot)

            botcount -= 1
            if botcount > 0:
                osd(bot, botcom.channel_current, 'say', "     ")

        else:
            cannotproceed.append(targetbot)

    if cannotproceed != []:
        osd(bot, botcom.channel_current, 'say', spicemanip(bot, cannotproceed, 'andlist') + " could not be restarted.")


def bot_nickcom_function_debug(bot, botcom):

    targetbots = {}
    if botcom.triggerargsarray == []:
        targetbots[str(bot.nick)] = dict()
    elif 'all' in botcom.triggerargsarray:
        for targetbot in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
            targetbots[targetbot] = dict()
    else:
        for targetbot in botcom.triggerargsarray:
            if targetbot in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
                targetbots[targetbot] = dict()

    osd(bot, botcom.channel_current, 'action', "Is Examining Log(s) for " + spicemanip(bot, targetbots.keys(), 'andlist'))

    for targetbot in targetbots.keys():

        debuglines = []
        ignorearray = ["COMMAND=/usr/sbin/service", "pam_unix(sudo:session)", "COMMAND=/bin/chown", "Docs: http://sopel.chat/", "Main PID:", "systemctl status", "sudo service"]
        for line in os.popen("sudo service " + targetbot + " status").read().split('\n'):
            if not any(x in str(line) for x in ignorearray):
                debuglines.append(str(line))

        targetbots[targetbot]['debuglines'] = debuglines

    botcount = len(targetbots.keys())
    nobotlogs = []
    for targetbot in targetbots.keys():
        if targetbots[targetbot]['debuglines'] != []:
            for line in targetbots[targetbot]['debuglines']:
                osd(bot, botcom.channel_current, 'say', line)
            botcount -= 1
            if botcount > 0:
                osd(bot, botcom.channel_current, 'say', "     ")
        else:
            nobotlogs.append(targetbot)

    if nobotlogs != []:
        osd(bot, botcom.channel_current, 'say', spicemanip(bot, nobotlogs, 'andlist') + " had no log(s) for some reason")


def bot_nickcom_function_permfix(bot, botcom):
    os.system("sudo chown -R spicebot:sudo /home/spicebot/.sopel/")
    osd(bot, botcom.channel_current, 'say', "Permissions should now be fixed")


def bot_nickcom_function_pip(bot, botcom):

    pipcoms = ['install', 'remove']
    subcom = spicemanip(bot, [x for x in botcom.triggerargsarray if x in pipcoms], 1) or None
    if not subcom:
        return osd(bot, trigger.sender, 'say', "pip requires a subcommand. Valid options: " + spicemanip(bot, pipcoms, 'andlist'))

    if subcom in botcom.triggerargsarray:
        botcom.triggerargsarray.remove(subcom)

    pippackage = spicemanip(bot, botcom.triggerargsarray, 0)
    if not pippackage:
        return osd(bot, botcom.channel_current, 'say', "You must specify a pip package.")

    installines = []
    previouslysatisfied = []
    for line in os.popen("sudo pip " + str(subcom) + " " + str(pippackage)).read().split('\n'):
        if "Requirement already satisfied:" in str(line):
            packagegood = str(line).split("Requirement already satisfied:", 1)[1]
            packagegood = str(packagegood).split("in", 1)[0]
            previouslysatisfied.append(packagegood)
        else:
            installines.append(str(line))

    if previouslysatisfied != []:
        previouslysatisfiedall = spicemanip(bot, previouslysatisfied, 'andlist')
        installines.insert(0, "The following required packages have already been satisfied: " + previouslysatisfiedall)

    if installines == []:
        return osd(bot, botcom.channel_current, 'action', "has no install log for some reason.")

    for line in installines:
        osd(bot, trigger.sender, 'say', line)
    osd(bot, botcom.channel_current, 'say', "Possibly done.")


"""
Directory Browsing
"""


def bot_nickcom_function_gitpull(bot, botcom):

    botcom.directory = get_nick_value(bot, botcom.instigator, 'current_admin_dir', longevity='temp') or bot.memory["botdict"]["tempvals"]['bots_list'][str(bot.nick)]['directory']
    osd(bot, botcom.channel_current, 'say', "attempting to git pull " + botcom.directory)
    g = git.cmd.Git(botcom.directory)
    g.pull()


def bot_nickcom_function_dir(bot, botcom):

    botcom.directory = get_nick_value(bot, botcom.instigator, 'current_admin_dir', longevity='temp') or bot.memory["botdict"]["tempvals"]['bots_list'][str(bot.nick)]['directory']
    botcom = bot_list_directory(bot, botcom)
    if botcom.directory == []:
        osd(bot, botcom.channel_current, 'say', "It appears this directory is empty.")
        return
    displaymsgarray = []
    displaymsgarray.append("Current files located in " + str(botcom.directory) + " :")
    for filename, filefoldertype in zip(botcom.directory_listing, botcom.filefoldertype):
        displaymsgarray.append(str("["+filefoldertype.title()+"] ")+str(filename))
    osd(bot, botcom.channel_current, 'say', displaymsgarray)


def bot_nickcom_function_cd(bot, botcom):

    validfolderoptions = ['..', 'reset']
    botcom.directory = get_nick_value(bot, botcom.instigator, 'current_admin_dir', longevity='temp') or bot.memory["botdict"]["tempvals"]['bots_list'][str(bot.nick)]['directory']
    botcom = bot_list_directory(bot, botcom)

    for filename, filefoldertype in zip(botcom.directory_listing, botcom.filefoldertype):
        if filefoldertype == 'folder':
            validfolderoptions.append(filename)

    movepath = spicemanip(bot, botcom.triggerargsarray, 0)
    if movepath not in validfolderoptions:
        if movepath in botcom.directory_listing and movepath not in validfolderoptions:
            osd(bot, botcom.channel_current, 'say', "You can't Change Directory into a File!")
        else:
            osd(bot, botcom.channel_current, 'say', "Invalid Folder Path")
        return

    if movepath == "..":
        movepath = os.path.dirname(botcom.directory)
    elif movepath == 'reset':
        movepath = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    else:
        movepath = os.path.join(botcom.directory, str(movepath+"/"))

    set_nick_value(bot, botcom.instigator, 'current_admin_dir', str(movepath), longevity='temp')

    osd(bot, botcom.channel_current, 'say', "Directory Changed to : " + str(movepath))


"""
Github
"""


def bot_nickcom_function_github(bot, botcom):
    osd(bot, botcom.channel_current, 'say', 'IRC Modules Repository     https://github.com/SpiceBot/SpiceBot')


def bot_nickcom_function_docs(bot, botcom):
    osd(bot, botcom.channel_current, 'say', "Online Docs: " + GITWIKIURL)


def bot_nickcom_function_help(bot, botcom):
    osd(bot, botcom.channel_current, 'say', "Online Docs: " + GITWIKIURL)


"""
Messaging channels
"""


def bot_nickcom_function_msg(bot, botcom):

    # Channel
    targetchannels = []
    targetword = spicemanip(bot, botcom.triggerargsarray, 1)
    if targetword not in bot.memory["botdict"]["tempvals"]['channels_list'].keys() and targetword != 'all':
        if botcom.channel_current.startswith('#'):
            targetchannels.append(botcom.channel_current)
        else:
            osd(bot, botcom.instigator, 'notice', "You must specify a valid channel.")
            return
    elif targetword == 'all':
        botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+', 'list')
        for targetchan in bot.memory["botdict"]["tempvals"]['channels_list'].keys():
            targetchannels.append(targetchan)
    else:
        for targetchan in botcom.triggerargsarray:
            if targetchan in bot.memory["botdict"]["tempvals"]['channels_list'].keys():
                targetchannels.append(targetchan)

    for channeltarget in targetchannels:
        if channeltarget in botcom.triggerargsarray:
            botcom.triggerargsarray.remove(channeltarget)

    botmessage = spicemanip(bot, botcom.triggerargsarray, 0)
    if not botmessage:
        osd(bot, botcom.instigator, 'notice', "You must specify a message.")
        return

    osd(bot, targetchannels, 'say', botmessage)


def bot_nickcom_function_action(bot, botcom):

    # Channel
    targetchannels = []
    targetword = spicemanip(bot, botcom.triggerargsarray, 1)
    if targetword not in bot.memory["botdict"]["tempvals"]['channels_list'].keys() and targetword != 'all':
        if botcom.channel_current.startswith('#'):
            targetchannels.append(botcom.channel_current)
        else:
            osd(bot, botcom.instigator, 'notice', "You must specify a valid channel.")
            return
    elif targetword == 'all':
        botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+', 'list')
        for targetchan in bot.memory["botdict"]["tempvals"]['channels_list'].keys():
            targetchannels.append(targetchan)
    else:
        for targetchan in botcom.triggerargsarray:
            if targetchan in bot.memory["botdict"]["tempvals"]['channels_list'].keys():
                targetchannels.append(targetchan)

    for channeltarget in targetchannels:
        if channeltarget in botcom.triggerargsarray:
            botcom.triggerargsarray.remove(channeltarget)

    botmessage = spicemanip(bot, botcom.triggerargsarray, 0)
    if not botmessage:
        osd(bot, botcom.instigator, 'notice', "You must specify a message.")
        return

    osd(bot, targetchannels, 'action', botmessage)


def bot_nickcom_function_notice(bot, botcom):

    # Target
    targets = []
    targetword = spicemanip(bot, botcom.triggerargsarray, 1)
    if targetword not in bot.memory["botdict"]["tempvals"]['all_current_users'] and targetword != 'all':
        if botcom.channel_current.startswith('#'):
            targets.append(botcom.channel_current)
        else:
            osd(bot, botcom.instigator, 'notice', "You must specify a valid target.")
            return
    elif targetword == 'all':
        botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+', 'list')
        for target in bot.memory["botdict"]["tempvals"]['all_current_users']:
            targets.append(target)
    else:
        for target in botcom.triggerargsarray:
            if target in bot.memory["botdict"]["tempvals"]['all_current_users']:
                targets.append(target)

    for target in targets:
        if target in botcom.triggerargsarray:
            botcom.triggerargsarray.remove(target)

    botmessage = spicemanip(bot, botcom.triggerargsarray, 0)
    if not botmessage:
        osd(bot, botcom.instigator, 'notice', "You must specify a message.")
        return

    osd(bot, targets, 'notice', botmessage)


"""
Channel
"""


def bot_nickcom_function_channel(bot, botcom):

    # SubCommand used
    valid_subcommands = ['list', 'op', 'hop', 'voice', 'owner', 'admin', 'users']
    subcommand = spicemanip(bot, [x for x in botcom.triggerargsarray if x.lower() in valid_subcommands], 1) or 'list'
    if subcommand in botcom.triggerargsarray:
        botcom.triggerargsarray.remove(subcommand)
    subcommand = subcommand.lower()

    # list channels
    if subcommand == 'list':
        chanlist = spicemanip(bot, bot.memory["botdict"]["tempvals"]['channels_list'].keys(), 'andlist')
        osd(bot, botcom.channel_current, 'say', "You can find me in " + chanlist)
        return

    # Channel
    targetchannels = []
    if botcom.triggerargsarray == []:
        if botcom.channel_current.startswith('#'):
            targetchannels.append(botcom.channel_current)
        else:
            osd(bot, botcom.instigator, 'notice', "You must specify a valid channel.")
            return
    elif 'all' in botcom.triggerargsarray:
        for targetchan in bot.memory["botdict"]["tempvals"]['channels_list'].keys():
            targetchannels.append(targetchan)
    else:
        for targetchan in botcom.triggerargsarray:
            if targetchan in bot.memory["botdict"]["tempvals"]['channels_list'].keys():
                targetchannels.append(targetchan)

    dispmsg = []

    # OP list
    if subcommand.lower() == 'op':
        for channeltarget in targetchannels:
            if bot.memory["botdict"]["tempvals"]['channels_list'][channeltarget]['chanops'] == []:
                dispmsg.append("There are no Channel Operators for " + str(channeltarget))
            else:
                oplist = spicemanip(bot, bot.memory["botdict"]["tempvals"]['channels_list'][channeltarget]['chanops'], 'andlist')
                dispmsg.append("Channel Operators for " + str(channeltarget) + "  are: " + oplist)
        osd(bot, botcom.instigator, 'notice', spicemanip(bot, dispmsg, 'andlist'))
        return

    # HOP list
    if subcommand.lower() == 'hop':
        for channeltarget in targetchannels:
            if bot.memory["botdict"]["tempvals"]['channels_list'][channeltarget]['chanhalfops'] == []:
                dispmsg.append("There are no Channel Half Operators for " + str(channeltarget))
            else:
                hoplist = spicemanip(bot, bot.memory["botdict"]["tempvals"]['channels_list'][channeltarget]['chanhalfops'], 'andlist')
                dispmsg.append("Channel Half Operators for " + str(channeltarget) + "  are: " + hoplist)
        osd(bot, botcom.instigator, 'notice', spicemanip(bot, dispmsg, 'andlist'))
        return

    # Voice List
    if subcommand.lower() == 'voice':
        for channeltarget in targetchannels:
            if bot.memory["botdict"]["tempvals"]['channels_list'][channeltarget]['chanvoices'] == []:
                dispmsg.append("There are no Channel VOICE for " + str(channeltarget))
            else:
                voicelist = spicemanip(bot, bot.memory["botdict"]["tempvals"]['channels_list'][channeltarget]['chanvoices'], 'andlist')
                dispmsg.append("Channel VOICE for " + str(channeltarget) + " are: " + voicelist)
        osd(bot, botcom.instigator, 'notice', spicemanip(bot, dispmsg, 'andlist'))
        return

    # owner List
    if subcommand.lower() == 'owner':
        for channeltarget in targetchannels:
            if bot.memory["botdict"]["tempvals"]['channels_list'][channeltarget]['chanowners'] == []:
                dispmsg.append("There are no Channel OWNER for " + str(channeltarget))
            else:
                ownerlist = spicemanip(bot, bot.memory["botdict"]["tempvals"]['channels_list'][channeltarget]['chanowners'], 'andlist')
                dispmsg.append("Channel OWNER for " + str(channeltarget) + " are: " + ownerlist)
        osd(bot, botcom.instigator, 'notice', spicemanip(bot, dispmsg, 'andlist'))
        return

    # admin List
    if subcommand.lower() == 'admin':
        for channeltarget in targetchannels:
            if bot.memory["botdict"]["tempvals"]['channels_list'][channeltarget]['chanadmins'] == []:
                dispmsg.append("There are no Channel ADMIN for " + str(channeltarget))
            else:
                adminlist = spicemanip(bot, bot.memory["botdict"]["tempvals"]['channels_list'][channeltarget]['chanadmins'], 'andlist')
                dispmsg.append("Channel ADMIN for " + str(channeltarget) + " are: " + adminlist)
        osd(bot, botcom.instigator, 'notice', spicemanip(bot, dispmsg, 'andlist'))
        return

    # Users List
    if subcommand.lower() == 'users':
        for channeltarget in targetchannels:
            if bot.memory["botdict"]["tempvals"]['channels_list'][channeltarget]['current_users'] == []:
                dispmsg.append("There are no Channel users for " + str(channeltarget))
            else:
                userslist = spicemanip(bot, bot.memory["botdict"]["tempvals"]['channels_list'][channeltarget]['current_users'], 'andlist')
                dispmsg.append("Channel users for " + str(channeltarget) + " are: " + userslist)
        osd(bot, botcom.instigator, 'notice', spicemanip(bot, dispmsg, 'andlist'))
        return


"""
Permissions
"""


def bot_nickcom_function_admins(bot, botcom):

    targetbots = []
    if botcom.triggerargsarray == []:
        targetbots.append(str(bot.nick))
    elif 'all' in botcom.triggerargsarray:
        for targetbot in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
            targetbots.append(targetbot)
    else:
        for targetbot in botcom.triggerargsarray:
            if targetbot in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
                targetbots.append(targetbot)

    dispmsg = []
    for targetbot in targetbots:
        currentbotsadmins = bot.memory["botdict"]["tempvals"]['bots_list'][targetbot]['configuration']['core']['admins']
        dispmsg.append(targetbot + " is administered by " + currentbotsadmins)
    osd(bot, botcom.channel_current, 'say', spicemanip(bot, dispmsg, 'andlist'))


def bot_nickcom_function_owner(bot, botcom):

    targetbots = []
    if botcom.triggerargsarray == []:
        targetbots.append(str(bot.nick))
    elif 'all' in botcom.triggerargsarray:
        for targetbot in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
            targetbots.append(targetbot)
    else:
        for targetbot in botcom.triggerargsarray:
            if targetbot in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
                targetbots.append(targetbot)

    dispmsg = []
    for targetbot in targetbots:
        currentbotsowner = bot.memory["botdict"]["tempvals"]['bots_list'][targetbot]['configuration']['core']['owner']
        dispmsg.append(targetbot + " is owned by " + currentbotsowner)
    osd(bot, botcom.channel_current, 'say', spicemanip(bot, dispmsg, 'andlist'))


"""
Uptime
"""


def bot_nickcom_function_uptime(bot, botcom):
    delta = datetime.timedelta(seconds=round((datetime.datetime.utcnow() - bot.memory["botdict"]["tempvals"]["uptime"]).total_seconds()))
    osd(bot, botcom.channel_current, 'say', "I've been sitting here for {} and I keep going!".format(delta))


"""
Gender
"""


def bot_nickcom_function_gender(bot, botcom):
    osd(bot, botcom.channel_current, 'say', "My gender is Female")


"""
Can You see me
"""


def bot_nickcom_function_canyouseeme(bot, botcom):
    osd(bot, botcom.channel_current, 'say', botcom.instigator + ", I can see you.")


"""
Dictionary commands
"""


def bot_dictcom_handle(bot, botcom):

    # command aliases
    if "aliasfor" in bot.memory["botdict"]["tempvals"]['dict_commands'][botcom.dotcommand].keys():
        botcom.dotcommand = bot.memory["botdict"]["tempvals"]['dict_commands'][botcom.dotcommand]["aliasfor"]

    # simplify usage of the bot command going forward
    # botcom.dotcommand_dict = bot.memory["botdict"]["tempvals"]['dict_commands'][botcom.dotcommand].copy()
    botcom.dotcommand_dict = copy.deepcopy(bot.memory["botdict"]["tempvals"]['dict_commands'][botcom.dotcommand])

    # remainder, if any is the new arg list
    botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+')

    # patch for people typing "...", maybe other stuff, but this verifies that there is still a command here
    if not botcom.dotcommand:
        return

    botcom.maincom = botcom.dotcommand_dict["validcoms"][0]

    # execute function based on command type
    botcom.commandtype = botcom.dotcommand_dict["type"].lower()

    # IF "&&" is in the full input, it is treated as multiple commands, and is split
    commands_array = spicemanip(bot, botcom.triggerargsarray, "split_&&")
    if commands_array == []:
        commands_array = [[]]
    for command_split_partial in commands_array:
        botcom.triggerargsarray = spicemanip(bot, command_split_partial, 'create')

        # bot_dictcom_simple(bot, botcom)  # TODO rename
        botcom.completestring = spicemanip(bot, botcom.triggerargsarray, 0)

        bot_dictcom_process(bot, botcom)


def bot_dictcom_process(bot, botcom):

    # use the default key, unless otherwise specified
    botcom.responsekey = "?default"

    # handling for special cases
    posscom = spicemanip(bot, botcom.triggerargsarray, 1)
    if posscom.lower() in [command.lower() for command in botcom.dotcommand_dict.keys()]:
        for command in botcom.dotcommand_dict.keys():
            if command.lower() == posscom.lower():
                posscom = command
        botcom.responsekey = posscom
        botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+', 'list')
    botcom.commandtype = botcom.dotcommand_dict[botcom.responsekey]["type"]

    # This allows users to specify which reply by number by using an ! and a digit (first or last in string)
    validspecifides = ['last', 'random', 'count', 'view', 'add', 'del', 'remove', 'special', 'contrib', "contributors", 'author', "alias", "filepath", "enable", "disable"]
    botcom.specified = None
    argone = spicemanip(bot, botcom.triggerargsarray, 1)
    if str(argone).startswith("--") and len(str(argone)) > 2:
        if str(argone[2:]).isdigit() or str(argone[2:]) in validspecifides:
            botcom.specified = argone[2:]
        else:
            try:
                botcom.specified = w2n.word_to_num(str(argone[1:]))
            except ValueError:
                botcom.specified = None
        if botcom.specified:
            botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+', 'list')

    if botcom.specified:
        if str(botcom.specified).isdigit():
            botcom.specified = int(botcom.specified)

    # commands that can be updated
    if botcom.dotcommand_dict[botcom.responsekey]["updates_enabled"]:
        if botcom.dotcommand_dict[botcom.responsekey]["updates_enabled"] == "shared":
            adjust_nick_array(bot, str(bot.nick), botcom.maincom + "_" + str(botcom.responsekey), botcom.dotcommand_dict[botcom.responsekey]["responses"], 'startup', 'long', 'sayings')
            botcom.dotcommand_dict[botcom.responsekey]["responses"] = get_nick_value(bot, str(bot.nick), botcom.dotcommand_dict["validcoms"][0] + "_" + str(botcom.responsekey), 'long', 'sayings') or []
        elif botcom.dotcommand_dict[botcom.responsekey]["updates_enabled"] == "user":
            adjust_nick_array(bot, str(botcom.instigator), botcom.maincom + "_" + str(botcom.responsekey), botcom.dotcommand_dict[botcom.responsekey]["responses"], 'startup', 'long', 'sayings')
            botcom.dotcommand_dict[botcom.responsekey]["responses"] = get_nick_value(bot, str(botcom.instigator), botcom.dotcommand_dict["validcoms"][0] + "_" + str(botcom.responsekey), 'long', 'sayings') or []

    # Hardcoded commands Below
    if botcom.specified == 'enable':

        if not botcom.channel_current.startswith('#'):
            return osd(bot, botcom.instigator, 'notice', "This command must be run in the channel you which to " + botcom.specified + " it in.")

        if botcom.maincom not in bot.memory["botdict"]['channels_list'][str(botcom.channel_current)]["disabled_commands"].keys():
            return osd(bot, botcom.channel_current, 'say', botcom.maincom + " is already " + botcom.specified + "d in " + str(botcom.channel_current))

        commandrunconsensus, commandrun = [], True
        if botcom.instigator not in bot.memory["botdict"]["tempvals"]['bot_admins']:
            commandrunconsensus.append('False')
        else:
            commandrunconsensus.append('True')
        if botcom.instigator not in bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['chanops']:
            commandrunconsensus.append('False')
        else:
            commandrunconsensus.append('True')
        if botcom.instigator not in bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['chanowners']:
            commandrunconsensus.append('False')
        else:
            commandrunconsensus.append('True')
        if botcom.instigator not in bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['chanadmins']:
            commandrunconsensus.append('False')
        else:
            commandrunconsensus.append('True')
        if 'True' not in commandrunconsensus:
            commandrun = False
        if not commandrun:
            return osd(bot, botcom.channel_current, 'say', "You are not authorized to " + botcom.specified + " " + botcom.maincom + " in " + str(botcom.channel_current))

        del bot.memory["botdict"]['channels_list'][str(botcom.channel_current)]["disabled_commands"][botcom.maincom]
        return osd(bot, botcom.channel_current, 'say', botcom.maincom + " is now " + botcom.specified + "d in " + str(botcom.channel_current))

    elif botcom.specified == 'disable':

        if not botcom.channel_current.startswith('#'):
            return osd(bot, botcom.instigator, 'notice', "This command must be run in the channel you which to " + botcom.specified + " it in.")

        if botcom.maincom in bot.memory["botdict"]['channels_list'][str(botcom.channel_current)]["disabled_commands"].keys():
            return osd(bot, botcom.channel_current, 'say', botcom.maincom + " is already " + botcom.specified + "d in " + str(botcom.channel_current))

        commandrunconsensus, commandrun = [], True
        if botcom.instigator not in bot.memory["botdict"]["tempvals"]['bot_admins']:
            commandrunconsensus.append('False')
        else:
            commandrunconsensus.append('True')
        if botcom.instigator not in bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['chanops']:
            commandrunconsensus.append('False')
        else:
            commandrunconsensus.append('True')
        if botcom.instigator not in bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['chanowners']:
            commandrunconsensus.append('False')
        else:
            commandrunconsensus.append('True')
        if botcom.instigator not in bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['chanadmins']:
            commandrunconsensus.append('False')
        else:
            commandrunconsensus.append('True')
        if 'True' not in commandrunconsensus:
            commandrun = False
        if not commandrun:
            return osd(bot, botcom.channel_current, 'say', "You are not authorized to " + botcom.specified + " " + botcom.maincom + " in " + str(botcom.channel_current))

        trailingmessage = spicemanip(bot, botcom.triggerargsarray, 0) or "No reason given."
        timestamp = str(datetime.datetime.utcnow())
        bot.memory["botdict"]['channels_list'][str(botcom.channel_current)]["disabled_commands"][botcom.maincom] = {"reason": trailingmessage, "timestamp": timestamp, "disabledby": botcom.instigator}
        return osd(bot, botcom.channel_current, 'say', botcom.maincom + " is now " + botcom.specified + "d in " + str(botcom.channel_current) + " at " + str(timestamp) + " for the following reason: " + trailingmessage)

    elif botcom.specified == 'special':
        nonstockoptions = []
        for command in botcom.dotcommand_dict.keys():
            if command not in ["?default", "validcoms", "contributors", "author", "type", "filepath"]:
                nonstockoptions.append(command)
        nonstockoptions = spicemanip(bot, nonstockoptions, "andlist")
        return osd(bot, botcom.channel_current, 'say', "The special options for " + str(botcom.maincom) + " command include: " + str(nonstockoptions) + ".")

    elif botcom.specified == 'count':
        return osd(bot, botcom.channel_current, 'say', "The " + str(botcom.maincom) + " " + str(botcom.responsekey or '') + " command has " + str(len(botcom.dotcommand_dict[botcom.responsekey]["responses"])) + " entries.")

    elif botcom.specified == 'filepath':
        return osd(bot, botcom.channel_current, 'say', "The " + str(botcom.maincom) + " file is located at " + str(botcom.dotcommand_dict["filepath"]))

    elif botcom.specified == 'author':
        return osd(bot, botcom.channel_current, 'say', "The author of the " + str(botcom.maincom) + " command is " + botcom.dotcommand_dict["author"] + ".")

    elif botcom.specified in ['contrib', "contributors"]:
        return osd(bot, botcom.channel_current, 'say', "The contributors of the " + str(botcom.maincom) + " command are " + spicemanip(bot, botcom.dotcommand_dict["contributors"], "andlist") + ".")

    elif botcom.specified == 'alias':
        return osd(bot, botcom.channel_current, 'say', "The alaises of the " + str(botcom.maincom) + " command are " + spicemanip(bot, botcom.dotcommand_dict["validcoms"], "andlist") + ".")

    elif botcom.specified == 'view':
        if botcom.dotcommand_dict[botcom.responsekey]["responses"] == []:
            return osd(bot, botcom.channel_current, 'say', "The " + str(botcom.maincom) + " " + str(botcom.responsekey or '') + " command appears to have no entries!")
        else:
            osd(bot, botcom.instigator, 'notice', "The " + str(botcom.maincom) + " " + str(botcom.responsekey or '') + " command contains:")
            listnumb, relist = 1, []
            for item in botcom.dotcommand_dict[botcom.responsekey]["responses"]:
                if listnumb <= 20:
                    if isinstance(item, dict):
                        relist.append(str("[#" + str(listnumb) + "] COMPLEX dict Entry"))
                    elif isinstance(item, list):
                        relist.append(str("[#" + str(listnumb) + "] COMPLEX list Entry"))
                    else:
                        relist.append(str("[#" + str(listnumb) + "] " + str(item)))
                listnumb += 1
            osd(bot, botcom.instigator, 'say', relist)
            if listnumb > 20:
                osd(bot, botcom.instigator, 'say', "List cut off after the 20th entry to prevent bot lag.")
            return

    elif botcom.specified == 'add':

        if not botcom.dotcommand_dict[botcom.responsekey]["updates_enabled"]:
            return osd(bot, botcom.channel_current, 'say', "The " + str(botcom.maincom) + " " + str(botcom.responsekey or '') + " entry list cannot be updated.")

        fulltext = spicemanip(bot, botcom.triggerargsarray, 0)
        if not fulltext:
            return osd(bot, botcom.channel_current, 'say', "What would you like to add to the " + str(botcom.maincom) + " " + str(botcom.responsekey or '') + " entry list?")

        if fulltext in botcom.dotcommand_dict[botcom.responsekey]["responses"]:
            return osd(bot, botcom.channel_current, 'say', "The following was already in the " + str(botcom.maincom) + " " + str(botcom.responsekey or '') + " entry list: '" + str(fulltext) + "'")

        if botcom.dotcommand_dict[botcom.responsekey]["updates_enabled"] == "shared":
            adjust_nick_array(bot, str(bot.nick), botcom.maincom + "_" + str(botcom.responsekey), fulltext, botcom.specified, 'long', 'sayings')
        elif botcom.dotcommand_dict[botcom.responsekey]["updates_enabled"] == "user":
            adjust_nick_array(bot, str(botcom.instigator), botcom.maincom + "_" + str(botcom.responsekey), fulltext, botcom.specified, 'long', 'sayings')

        return osd(bot, botcom.channel_current, 'say', "The following was added to the " + str(botcom.maincom) + " " + str(botcom.responsekey or '') + " entry list: '" + str(fulltext) + "'")

    elif botcom.specified in ['del', 'remove']:

        if not botcom.dotcommand_dict[botcom.responsekey]["updates_enabled"]:
            return osd(bot, botcom.channel_current, 'say', "The " + str(botcom.maincom) + " " + str(botcom.responsekey or '') + " entry list cannot be updated.")

        fulltext = spicemanip(bot, botcom.triggerargsarray, 0)
        if not fulltext:
            return osd(bot, botcom.channel_current, 'say', "What would you like to remove from the " + str(botcom.maincom) + " " + str(botcom.responsekey or '') + " entry list?")

        if fulltext not in botcom.dotcommand_dict[botcom.responsekey]["responses"]:
            return osd(bot, botcom.channel_current, 'say', "The following was already not in the " + str(botcom.maincom) + " " + str(botcom.responsekey or '') + " entry list: '" + str(fulltext) + "'")

        if botcom.dotcommand_dict[botcom.responsekey]["updates_enabled"] == "shared":
            adjust_nick_array(bot, str(bot.nick), botcom.maincom + "_" + str(botcom.responsekey), fulltext, botcom.specified, 'long', 'sayings')
        elif botcom.dotcommand_dict[botcom.responsekey]["updates_enabled"] == "user":
            adjust_nick_array(bot, str(botcom.instigator), botcom.maincom + "_" + str(botcom.responsekey), fulltext, botcom.specified, 'long', 'sayings')

        return osd(bot, botcom.channel_current, 'say', "The following was removed from the " + str(botcom.maincom) + " " + str(botcom.responsekey or '') + " entry list: '" + str(fulltext) + "'")

    elif botcom.specified and not botcom.dotcommand_dict[botcom.responsekey]["selection_allowed"]:
        return osd(bot, botcom.channel_current, 'say', "The " + str(botcom.maincom) + " " + str(botcom.responsekey or '') + " response list cannot be specified.")

    botcom.target = False

    if str(botcom.channel_current).startswith('#'):
        if botcom.maincom in bot.memory["botdict"]['channels_list'][str(botcom.channel_current)]["disabled_commands"].keys():
            reason = bot.memory["botdict"]['channels_list'][str(botcom.channel_current)]["disabled_commands"][str(botcom.maincom)]["reason"]
            timestamp = bot.memory["botdict"]['channels_list'][str(botcom.channel_current)]["disabled_commands"][str(botcom.maincom)]["timestamp"]
            bywhom = bot.memory["botdict"]['channels_list'][str(botcom.channel_current)]["disabled_commands"][str(botcom.maincom)]["disabledby"]
            return osd(bot, botcom.channel_current, 'say', "The " + str(botcom.maincom) + " command was disabled by " + bywhom + " in " + str(botcom.channel_current) + " at " + str(timestamp) + " for the following reason: " + str(reason))

    # hardcoded_channel_block
    if str(botcom.channel_current).startswith('#'):
        if str(botcom.channel_current) in botcom.dotcommand_dict["hardcoded_channel_block"]:
            return osd(bot, botcom.channel_current, 'say', "The " + str(botcom.maincom) + " command cannot be used in " + str(botcom.channel_current) + " because it is hardcoded not to.")

    # hardcoded_channel_block
    if str(botcom.channel_current).startswith('#'):
        if str(botcom.channel_current) in botcom.dotcommand_dict[botcom.responsekey]["hardcoded_channel_block"]:
            return osd(bot, botcom.channel_current, 'say', "The " + str(botcom.maincom) + " " + str(botcom.responsekey or '') + " command cannot be used in " + str(botcom.channel_current) + " because it is hardcoded not to.")

    botcom.success = True
    if botcom.commandtype in ['simple', 'fillintheblank', "target", 'targetplusreason', 'sayings', "readfromfile", "readfromurl", "ascii_art", "translate", "responses"]:
        return bot_dictcom_responses(bot, botcom)
    else:
        command_function_run = str('bot_dictcom_' + botcom.commandtype + '(bot, botcom)')
        eval(command_function_run)


def bot_dictcom_responses(bot, botcom):

    commandrunconsensus = []
    reaction = False

    # A target is required
    if botcom.dotcommand_dict[botcom.responsekey]["target_required"]:

        # try first term as a target
        posstarget = spicemanip(bot, botcom.triggerargsarray, 1) or 0
        targetbypass = botcom.dotcommand_dict[botcom.responsekey]["target_bypass"]
        targetchecking = bot_target_check(bot, botcom, posstarget, targetbypass)
        if not targetchecking["targetgood"]:

            if botcom.dotcommand_dict[botcom.responsekey]["target_backup"]:
                botcom.target = botcom.dotcommand_dict[botcom.responsekey]["target_backup"]
                if botcom.target == 'instigator':
                    botcom.target = botcom.instigator
                elif botcom.target == 'random':
                    botcom.target = bot_random_valid_target(bot, botcom, 'random')
            else:
                for reason in ['self', 'bot', 'bots', 'offline', 'unknown', 'privmsg', 'diffchannel']:
                    if targetchecking["reason"] == reason and botcom.dotcommand_dict[botcom.responsekey]["react_"+reason]:
                        reaction = True
                        commandrunconsensus.append(botcom.dotcommand_dict[botcom.responsekey]["react_"+reason])
                if not reaction:
                    commandrunconsensus.append([targetchecking["error"]])
        else:
            botcom.target = spicemanip(bot, botcom.triggerargsarray, 1)
            botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+', 'list')

    # $blank input
    botcom.completestring = spicemanip(bot, botcom.triggerargsarray, 0) or ''
    if botcom.dotcommand_dict[botcom.responsekey]["blank_required"]:

        if botcom.completestring == '' or not botcom.completestring:

            if botcom.dotcommand_dict[botcom.responsekey]["blank_backup"]:
                botcom.completestring = botcom.dotcommand_dict[botcom.responsekey]["blank_backup"]
            else:
                commandrunconsensus.append(botcom.dotcommand_dict[botcom.responsekey]["blank_fail"])

        if botcom.dotcommand_dict[botcom.responsekey]["blank_phrasehandle"]:
            if botcom.dotcommand_dict[botcom.responsekey]["blank_phrasehandle"] != []:
                if spicemanip(bot, botcom.completestring, 1).lower() not in botcom.dotcommand_dict[botcom.responsekey]["blank_phrasehandle"]:
                    botcom.completestring = botcom.dotcommand_dict[botcom.responsekey]["blank_phrasehandle"][0] + " " + botcom.completestring
                elif spicemanip(bot, botcom.completestring, 1).lower() in botcom.dotcommand_dict[botcom.responsekey]["blank_phrasehandle"]:
                    if spicemanip(bot, botcom.completestring, 1).lower() != botcom.dotcommand_dict[botcom.responsekey]["blank_phrasehandle"][0]:
                        botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+', 'list')
                        if botcom.triggerargsarray != []:
                            botcom.completestring = botcom.dotcommand_dict[botcom.responsekey]["blank_phrasehandle"][0] + " " + spicemanip(bot, botcom.triggerargsarray, 0)

    if commandrunconsensus != []:
        botcom.success = False
        if botcom.dotcommand_dict[botcom.responsekey]["response_fail"] and not reaction:
            botcom.dotcommand_dict[botcom.responsekey]["responses"] = botcom.dotcommand_dict[botcom.responsekey]["response_fail"]
        else:
            botcom.dotcommand_dict[botcom.responsekey]["responses"] = commandrunconsensus[0]

    bot_dictcom_reply_shared(bot, botcom)


def bot_dictcom_reply_shared(bot, botcom):

    if botcom.specified:
        if botcom.specified > len(botcom.dotcommand_dict[botcom.responsekey]["responses"]):
            currentspecified = len(botcom.dotcommand_dict[botcom.responsekey]["responses"])
        else:
            currentspecified = botcom.specified
        botcom.replies = spicemanip(bot, botcom.dotcommand_dict[botcom.responsekey]["responses"], currentspecified, 'return')
    else:
        botcom.replies = spicemanip(bot, botcom.dotcommand_dict[botcom.responsekey]["responses"], 'random', 'return')

    # This handles responses in list form
    if not isinstance(botcom.replies, list):
        botcom.replies = [botcom.replies]

    for rply in botcom.replies:

        # replies that can be evaluated as code
        if rply.startswith("time.sleep"):
            eval(rply)
        else:

            # random number
            if "$randnum" in rply:
                if botcom.dotcommand_dict[botcom.responsekey]["randnum"]:
                    randno = randint(botcom.dotcommand_dict[botcom.responsekey]["randnum"][0], botcom.dotcommand_dict[botcom.responsekey]["randnum"][1])
                else:
                    randno = randint(0, 50)
                rply = rply.replace("$randnum", str(randno))

            # blank
            if "$blank" in rply:
                rply = rply.replace("$blank", botcom.completestring or '')

            # the remaining input
            if "$input" in rply:
                rply = rply.replace("$input", spicemanip(bot, botcom.triggerargsarray, 0) or botcom.maincom)

            # translation
            if botcom.dotcommand_dict[botcom.responsekey]["translations"]:
                rply = bot_translate_process(bot, rply, botcom.dotcommand_dict[botcom.responsekey]["translations"])

            # text to precede the output
            if botcom.dotcommand_dict[botcom.responsekey]["prefixtext"] and botcom.success:
                rply = spicemanip(bot, botcom.dotcommand_dict[botcom.responsekey]["prefixtext"], 'random') + rply

            # text to follow the output
            if botcom.dotcommand_dict[botcom.responsekey]["suffixtext"] and botcom.success:
                rply = rply + spicemanip(bot, botcom.dotcommand_dict[botcom.responsekey]["suffixtext"], 'random')

            # trigger.nick
            if "$instigator" in rply:
                rply = rply.replace("$instigator", botcom.instigator or '')

            # random user
            if "$randuser" in rply:
                randuser = spicemanip(bot, bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['current_users'], 'random')
                rply = rply.replace("$randuser", randuser)

            # current channel
            if "$channel" in rply:
                rply = rply.replace("$channel", botcom.channel_current or '')

            # bot.nick
            if "$botnick" in rply:
                rply = rply.replace("$botnick", bot.nick or '')

            # target
            if "$target" in rply:
                targetnames = botcom.target or ''
                if "$targets" in rply:
                    if targetnames.lower() == "your":
                        targetnames = targetnames
                    elif targetnames.endswith("s"):
                        targetnames = targetnames + "'"
                    else:
                        targetnames = targetnames + "s"
                    rply = rply.replace("$targets", targetnames)
                else:
                    targetnames = targetnames
                    rply = rply.replace("$target", targetnames)

            # smaller variations for the text
            if "$replyvariation" in rply:
                if botcom.dotcommand_dict[botcom.responsekey]["replyvariation"] != []:
                    variation = spicemanip(bot, botcom.dotcommand_dict[botcom.responsekey]["replyvariation"], 'random')
                    rply = rply.replace("$replyvariation", variation)
                else:
                    rply = rply.replace("$replyvariation", '')

            # display special options for this command
            if "$specialoptions" in rply:
                nonstockoptions = []
                for command in botcom.dotcommand_dict.keys():
                    if command not in ["?default", "validcoms", "contributors", "author", "type", "filepath"]:
                        nonstockoptions.append(command)
                nonstockoptions = spicemanip(bot, nonstockoptions, "andlist")
                rply = rply.replace("$specialoptions", nonstockoptions)

            # saying, or action?
            if rply.startswith("*a "):
                rplytype = 'action'
                rply = rply.replace("*a ", "")
            else:
                rplytype = 'say'

            osd(bot, botcom.channel_current, rplytype, rply)


def bot_dictcom_gif(bot, botcom):

    if botcom.dotcommand_dict[botcom.responsekey]["blank_required"] and not botcom.completestring:
        botcom.dotcommand_dict[botcom.responsekey]["responses"] = botcom.dotcommand_dict[botcom.responsekey]["blank_fail"]
        return bot_dictcom_reply_shared(bot, botcom)
    elif botcom.dotcommand_dict[botcom.responsekey]["blank_required"] and botcom.completestring:
        queries = [botcom.completestring]
    else:
        queries = botcom.dotcommand_dict[botcom.responsekey]["responses"]

    # which api's are we using to search
    if botcom.dotcommand in bot.memory["botdict"]["tempvals"]['valid_gif_api_dict'].keys():
        searchapis = [botcom.dotcommand]
    elif "queryapi" in botcom.dotcommand_dict.keys():
        searchapis = botcom.dotcommand_dict[botcom.responsekey]["queryapi"]
    else:
        searchapis = bot.memory["botdict"]["tempvals"]['valid_gif_api_dict'].keys()

    if botcom.specified:
        if botcom.specified > len(queries):
            botcom.specified = len(queries)
        query = spicemanip(bot, queries, botcom.specified, 'return')
    else:
        query = spicemanip(bot, queries, 'random', 'return')

    searchdict = {"query": query, "gifsearch": searchapis}

    # nsfwenabled = get_database_value(bot, bot.nick, 'channels_nsfw') or []
    # if botcom.channel_current in nsfwenabled:
    #    searchdict['nsfw'] = True

    gifdict = getGif(bot, searchdict)

    if gifdict["error"]:
        botcom.success = False
        if botcom.dotcommand_dict[botcom.responsekey]["search_fail"]:
            gifdict["error"] = botcom.dotcommand_dict[botcom.responsekey]["search_fail"]
        botcom.dotcommand_dict[botcom.responsekey]["responses"] = [gifdict["error"]]
    else:
        botcom.dotcommand_dict[botcom.responsekey]["responses"] = [str(gifdict['gifapi'].title() + " Result (" + str(query) + " #" + str(gifdict["returnnum"]) + "): " + str(gifdict["returnurl"]))]

    botcom.specified = False
    bot_dictcom_reply_shared(bot, botcom)


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
# Bot Restart/Update
"""


def bot_restart(bot, targetbot):
    if bot.memory["botdict"]["tempvals"]['bots_list'][targetbot]['directory']:
        os.system("sudo service " + str(targetbot) + " restart")


def bot_update(bot, targetbot):
    if bot.memory["botdict"]["tempvals"]['bots_list'][targetbot]['directory']:
        g = git.cmd.Git(bot.memory["botdict"]["tempvals"]['bots_list'][targetbot]['directory'])
        g.pull()


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
Small Functions
"""


def nick_actual(bot, nick):
    nick_actual = nick
    if "botdict_loaded" not in bot.memory:
        for u in bot.users:
            if u.lower() == str(nick).lower():
                nick_actual = u
        return nick_actual
    for u in bot.memory["botdict"]["users"].keys():
        if u.lower() == str(nick).lower():
            nick_actual = u
    return nick_actual


def bot_random_valid_target(bot, botcom, outputtype):
    validtargs = []
    if not botcom.channel_current.startswith('#'):
        validtargs.extend([str(bot.nick), botcom.instigator])
    else:
        for user in bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['current_users']:
            targetchecking = bot_target_check(bot, botcom, user, [])
            if targetchecking["targetgood"]:
                validtargs.append(user)
    if outputtype == 'list':
        return validtargs
    elif outputtype == 'random':
        return spicemanip(bot, validtargs, 'random')


def bot_check_inlist(bot, searchterm, searchlist):

    # bot.msg("#spicebottest", str(searchterm))
    # bot.msg("#spicebottest", str(searchlist))

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
        if bot_check_inlist(bot, target, bot.memory["botdict"]["tempvals"]['bots_list'].keys()):
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
        if not bot_check_inlist(bot, target, bot.memory["botdict"]["tempvals"]['all_current_users']):
            return {"targetgood": False, "error": "It looks like " + nick_actual(bot, target) + " is offline right now!", "reason": "offline"}

    # Private Message
    if "privmsg" not in targetbypass:
        if not str(botcom.channel_current).startswith('#') and not bot_check_inlist(bot, target, botcom.instigator):
            return {"targetgood": False, "error": "Leave " + nick_actual(bot, target) + " out of this private conversation!", "reason": "privmsg"}

    # not in the same channel
    if "diffchannel" not in targetbypass:
        if str(botcom.channel_current).startswith('#') and bot_check_inlist(bot, target, bot.memory["botdict"]["tempvals"]['all_current_users']):
            if str(target).lower() not in [u.lower() for u in bot.memory["botdict"]["tempvals"]['channels_list'][str(botcom.channel_current)]['current_users']]:
                return {"targetgood": False, "error": "It looks like " + nick_actual(bot, target) + " is online right now, but in a different channel.", "reason": "diffchannel"}

    return targetgood


def ipv4detect(bot, hostIP):
    pat = re.compile("\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}")
    test = pat.match(hostIP)
    return test


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


# get nick value from bot.memory
def get_nick_value(bot, nick, secondarykey, longevity='long', mainkey='unsorted'):

    # verify nick dict exists
    if longevity == 'long':
        if nick not in bot.memory["botdict"]["users"].keys():
            bot.memory["botdict"]["users"][nick] = dict()
    elif longevity == 'temp':
        if nick not in bot.memory["botdict"]["tempvals"]["uservals"].keys():
            bot.memory["botdict"]["tempvals"]["uservals"][nick] = dict()

    # Verify mainkey exists
    if longevity == 'long':
        if mainkey not in bot.memory["botdict"]["users"][nick].keys():
            bot.memory["botdict"]["users"][nick][mainkey] = dict()
    elif longevity == 'temp':
        if mainkey not in bot.memory["botdict"]["tempvals"]["uservals"][nick].keys():
            bot.memory["botdict"]["tempvals"]["uservals"][nick][mainkey] = dict()

    # Verify secondarykey exists
    if longevity == 'long':
        if secondarykey not in bot.memory["botdict"]["users"][nick][mainkey].keys():
            return None
        else:
            return bot.memory["botdict"]["users"][nick][mainkey][secondarykey]
    elif longevity == 'temp':
        if secondarykey not in bot.memory["botdict"]["tempvals"]["uservals"][nick][mainkey].keys():
            return None
        else:
            return bot.memory["botdict"]["tempvals"]["uservals"][nick][mainkey][secondarykey]


# set nick value in bot.memory
def set_nick_value(bot, nick, secondarykey, value, longevity='long', mainkey='unsorted'):

    # verify nick dict exists
    if longevity == 'long':
        if nick not in bot.memory["botdict"]["users"].keys():
            bot.memory["botdict"]["users"][nick] = dict()
    elif longevity == 'temp':
        if nick not in bot.memory["botdict"]["tempvals"]["uservals"].keys():
            bot.memory["botdict"]["tempvals"]["uservals"][nick] = dict()

    # Verify mainkey exists
    if longevity == 'long':
        if mainkey not in bot.memory["botdict"]["users"][nick].keys():
            bot.memory["botdict"]["users"][nick][mainkey] = dict()
    elif longevity == 'temp':
        if mainkey not in bot.memory["botdict"]["tempvals"]["uservals"][nick].keys():
            bot.memory["botdict"]["tempvals"]["uservals"][nick][mainkey] = dict()

    # set
    if longevity == 'long':
        bot.memory["botdict"]["users"][nick][mainkey][secondarykey] = value
    elif longevity == 'temp':
        bot.memory["botdict"]["tempvals"]["uservals"][nick][mainkey][secondarykey] = value


# adjust a list of entries in bot.memory
def adjust_nick_array(bot, nick, secondarykey, values, direction, longevity='long', mainkey='unsorted'):

    if not isinstance(values, list):
        values = [values]

    # verify nick dict exists
    if longevity == 'long':
        if nick not in bot.memory["botdict"]["users"].keys():
            bot.memory["botdict"]["users"][nick] = dict()
    elif longevity == 'temp':
        if nick not in bot.memory["botdict"]["tempvals"]["uservals"].keys():
            bot.memory["botdict"]["tempvals"]["uservals"][nick] = dict()

    # Verify mainkey exists
    if longevity == 'long':
        if mainkey not in bot.memory["botdict"]["users"][nick].keys():
            bot.memory["botdict"]["users"][nick][mainkey] = dict()
    elif longevity == 'temp':
        if mainkey not in bot.memory["botdict"]["tempvals"]["uservals"][nick].keys():
            bot.memory["botdict"]["tempvals"]["uservals"][nick][mainkey] = dict()

    # verify array exists
    if longevity == 'long':
        if secondarykey not in bot.memory["botdict"]["users"][nick][mainkey]:
            bot.memory["botdict"]["users"][nick][mainkey][secondarykey] = []
    elif longevity == 'temp':
        if secondarykey not in bot.memory["botdict"]["tempvals"]["uservals"][nick][mainkey]:
            bot.memory["botdict"]["tempvals"]["uservals"][nick][mainkey][secondarykey] = []

    # startup entries
    if direction == 'startup':
        if longevity == 'long':
            if bot.memory["botdict"]["users"][nick][mainkey][secondarykey] == []:
                direction == 'add'
            else:
                return
        elif longevity == 'temp':
            if bot.memory["botdict"]["tempvals"]["uservals"][nick][mainkey][secondarykey] == []:
                direction == 'add'
            else:
                return

    # adjust
    for value in values:
        if longevity == 'long':
            if direction == 'add':
                if value not in bot.memory["botdict"]["users"][nick][mainkey][secondarykey]:
                    bot.memory["botdict"]["users"][nick][mainkey][secondarykey].append(value)
            elif direction == 'startup':
                if value not in bot.memory["botdict"]["users"][nick][mainkey][secondarykey]:
                    bot.memory["botdict"]["users"][nick][mainkey][secondarykey].append(value)
            elif direction in ['del', 'remove']:
                if value in bot.memory["botdict"]["users"][nick][mainkey][secondarykey]:
                    bot.memory["botdict"]["users"][nick][mainkey][secondarykey].remove(value)
        elif longevity == 'temp':
            if direction == 'add':
                if value not in bot.memory["botdict"]["tempvals"]["uservals"][nick][mainkey][secondarykey]:
                    bot.memory["botdict"]["tempvals"]["uservals"][nick][mainkey][secondarykey].append(value)
            elif direction == 'startup':
                if value not in bot.memory["botdict"]["tempvals"]["uservals"][nick][mainkey][secondarykey]:
                    bot.memory["botdict"]["tempvals"]["uservals"][nick][mainkey][secondarykey].append(value)
            elif direction in ['del', 'remove']:
                if value in bot.memory["botdict"]["tempvals"]["uservals"][nick][mainkey][secondarykey]:
                    bot.memory["botdict"]["tempvals"]["uservals"][nick][mainkey][secondarykey].remove(value)


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
                if len(textstring) > osd_limit:
                    chunks = textstring.split()
                    for chunk in chunks:
                        if currentstring == '':
                            currentstring = chunk
                        else:
                            tempstring = str(currentstring + " " + chunk)
                            if len(tempstring) <= osd_limit:
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
                elif len(textstring) > osd_limit:
                    if currentstring != '':
                        combinedtextarray.append(currentstring)
                        currentstring = ''
                    combinedtextarray.append(textstring)
                else:
                    tempstring = currentstring + "   " + textstring
                    if len(tempstring) <= osd_limit:
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
