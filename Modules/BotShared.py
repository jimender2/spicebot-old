#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
from sopel import module, tools
import sopel.module
from sopel.module import commands, nickname_commands, event, rule, OP, ADMIN, VOICE, HALFOP, thread, priority, example
from sopel.tools import Identifier
from sopel.tools.time import get_timezone, format_time

# imports for system and OS access, directories
import os
from os.path import exists
import sys

# Additional imports
import datetime
import time
import re
import random
import arrow
import fnmatch
import random
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
from random import randint


# user agent and header
ua = UserAgent()
header = {'User-Agent': str(ua.chrome)}


# Opening and reading config files
import ConfigParser


# Ensure Encoding
reload(sys)
sys.setdefaultencoding('utf-8')

"""
Variables # TODO add to botdict
"""


osd_limit = 420  # Ammount of text allowed to display per line

valid_com_types = ['simple', 'target', 'fillintheblank', 'targetplusreason', 'sayings', "readfromfile", "readfromurl", "ascii_art", "gif"]


"""
Bot Dictionaries
"""

bot_dict = {
                # Some values don't get saved to the database, but stay in memory
                "tempvals": {

                            # Indicate if we need to pull the dict from the database
                            "dict_loaded": False,

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

                }

# valid commands that the bot will reply to by name
valid_botnick_commands = {
                            "hithub": {
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
                            }

mode_dict_alias = {
                    "o": "OP",
                    "v": "VOICE",
                    "h": "HALFOP",
                    }


gif_dontusesites = [
                        "http://forgifs.com", "http://a.dilcdn.com", "http://www.bestgifever.com",
                        "http://s3-ec.buzzfed.com", "http://i.minus.com", "http://fap.to", "http://prafulla.net",
                        "http://3.bp.blogspot.com"
                        ]

gif_dontuseextensions = ['.jpg', '.png']


"""
Dict functions
"""


def botdict_open(bot):

    if "botdict_loaded" in bot.memory:
        return

    bot.memory["botdict"] = botdict_setup_open(bot)

    if not bot.memory["botdict"]["tempvals"]["uptime"]:
        bot.memory["botdict"]["tempvals"]["uptime"] = datetime.datetime.utcnow()

    # load external config file
    bot_external_config(bot)

    # Gif API
    bot_gif_api_access(bot)

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

    # use this to prevent bot usage if the above isn't done loading
    bot.memory["botdict_loaded"] = True

    # save dictionary now
    botdict_save(bot)


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
Saved Jobs Handling
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
Nick Commands
"""


def bot_nickcom_run(bot, trigger):

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

            if bot_command_run_check(bot, botcom):

                bot_command_function_run = str('bot_command_function_' + botcom.command_main.lower() + '(bot, botcom)')
                eval(bot_command_function_run)
            else:
                invalidcomslist.append(botcom.command_main)

    # Display Invalids coms used
    if invalidcomslist != []:
        osd(bot, botcom.instigator, 'notice', "I was unable to process the following Bot Nick commands due to privilege issues: " + spicemanip(bot, invalidcomslist, 'andlist'))


def bot_command_run_check(bot, botcom):
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

        if valid_botnick_commands[botcom.command_main.lower()]['privs'] == []:
            commandrunconsensus.append('True')

        if 'True' not in commandrunconsensus:
            commandrun = False

    return commandrun


"""
Basic Running Operations
"""


def bot_command_function_update(bot, botcom):

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


def bot_command_function_restart(bot, botcom):

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


def bot_command_function_debug(bot, botcom):

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


def bot_command_function_permfix(bot, botcom):
    os.system("sudo chown -R spicebot:sudo /home/spicebot/.sopel/")
    osd(bot, botcom.channel_current, 'say', "Permissions should now be fixed")


def bot_command_function_pip(bot, botcom):

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


def bot_command_function_gitpull(bot, botcom):

    botcom.directory = get_nick_value(bot, botcom.instigator, 'current_admin_dir', longevity='temp') or bot.memory["botdict"]["tempvals"]['bots_list'][str(bot.nick)]['directory']
    osd(bot, botcom.channel_current, 'say', "attempting to git pull " + botcom.directory)
    g = git.cmd.Git(botcom.directory)
    g.pull()


def bot_command_function_dir(bot, botcom):

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


def bot_command_function_cd(bot, botcom):

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


def bot_command_function_github(bot, botcom):
    osd(bot, botcom.channel_current, 'say', 'IRC Modules Repository     https://github.com/SpiceBot/SpiceBot')


def bot_command_function_docs(bot, botcom):
    osd(bot, botcom.channel_current, 'say', "Online Docs: " + GITWIKIURL)


def bot_command_function_help(bot, botcom):
    osd(bot, botcom.channel_current, 'say', "Online Docs: " + GITWIKIURL)


"""
Messaging channels
"""


def bot_command_function_msg(bot, botcom):

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


def bot_command_function_action(bot, botcom):

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


def bot_command_function_notice(bot, botcom):

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


def bot_command_function_channel(bot, botcom):

    # SubCommand used
    valid_subcommands = ['list', 'op', 'hop', 'voice', 'users']
    subcommand = spicemanip(bot, [x for x in botcom.triggerargsarray if x in valid_subcommands], 1) or 'list'
    if subcommand in botcom.triggerargsarray:
        botcom.triggerargsarray.remove(subcommand)

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


def bot_command_function_admins(bot, botcom):

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


def bot_command_function_owner(bot, botcom):

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


def bot_command_function_uptime(bot, botcom):
    delta = datetime.timedelta(seconds=round((datetime.datetime.utcnow() - bot.memory["botdict"]["tempvals"]["uptime"]).total_seconds()))
    osd(bot, botcom.channel_current, 'say', "I've been sitting here for {} and I keep going!".format(delta))


"""
Gender
"""


def bot_command_function_gender(bot, botcom):
    osd(bot, botcom.channel_current, 'say', "My gender is Female")


"""
Can You see me
"""


def bot_command_function_canyouseeme(bot, botcom):
    osd(bot, botcom.channel_current, 'say', botcom.instigator + ", I can see you.")


"""
Dictionary commands
"""


def bot_external_config(bot):

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


def bot_gif_api_access(bot):

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

    # iterate over organizational folders
    for quick_coms_type in os.listdir(quick_coms_path):

        # iterate over files within
        coms_type_file_path = os.path.join(quick_coms_path, quick_coms_type)
        for comconf in os.listdir(coms_type_file_path):

            # check if command file is already in the list
            if comconf not in bot.memory["botdict"]["tempvals"]['dict_commands_loaded']:
                bot.memory["botdict"]["tempvals"]['dict_commands_loaded'].append(comconf)

                # Read dictionary from file, if not, enable an empty dict
                inf = codecs.open(os.path.join(coms_type_file_path, comconf), "r", encoding='utf-8')
                infread = inf.read()
                try:
                    dict_from_file = eval(infread)
                except SyntaxError:
                    dict_from_file = dict()
                # Close File
                inf.close()

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

                if maincom not in bot.memory["botdict"]["tempvals"]['dict_commands'].keys():

                    # check that type is set
                    if "type" not in dict_from_file.keys():
                        dict_from_file["type"] = quick_coms_type.lower()
                    if dict_from_file["type"] not in valid_com_types:
                        dict_from_file["type"] = 'simple'
                        dict_from_file["replies"] = "This command is not setup with a proper 'type'."

                    # check that reply is set
                    if "replies" not in dict_from_file.keys():
                        if "filename" in dict_from_file.keys():
                            if dict_from_file["filename"] in bot.memory["botdict"]["tempvals"]['txt_files'].keys():
                                dict_from_file["replies"] = bot.memory["botdict"]["tempvals"]['txt_files'][dict_from_file["filename"]]
                        elif "readurl" in dict_from_file.keys():
                            page = requests.get(dict_from_file["readurl"], headers=header)
                            tree = html.fromstring(page.content)
                            if page.status_code == 200:
                                htmlfile = urllib.urlopen(dict_from_file["readurl"])
                                lines = htmlfile.read().splitlines()
                                dict_from_file["replies"] = lines
                        elif "defaultreplies" in dict_from_file.keys():
                                dict_from_file["replies"] = dict_from_file["defaultreplies"]
                        else:
                            dict_from_file["replies"] = "Reply missing"

                    if "updates_enabled" in dict_from_file.keys():
                        if dict_from_file["updates_enabled"]:
                            adjust_nick_array(bot, str(bot.nick), maincom + "_normal", dict_from_file["replies"], 'startup', 'long', 'sayings')

                    # make replies in list form if not
                    for mustbe in ["replies", "noinputreplies", "reasonhandle", "botreact"]:
                        if mustbe in dict_from_file.keys():
                            if not isinstance(dict_from_file[mustbe], list):
                                if dict_from_file[mustbe] in bot.memory["botdict"]["tempvals"]['txt_files'].keys():
                                    dict_from_file[mustbe] = bot.memory["botdict"]["tempvals"]['txt_files'][dict_from_file[mustbe]]
                                elif str(dict_from_file[mustbe]).startswith(tuple(["https://", "http://"])):
                                    page = requests.get(dict_from_file[mustbe], headers=header)
                                    tree = html.fromstring(page.content)
                                    if page.status_code == 200:
                                        htmlfile = urllib.urlopen(dict_from_file[mustbe])
                                        lines = htmlfile.read().splitlines()
                                        dict_from_file[mustbe] = lines
                                else:
                                    dict_from_file[mustbe] = [dict_from_file[mustbe]]

                    # Prefix text
                    if "prefixtext" not in dict_from_file.keys():
                        dict_from_file["prefixtext"] = False

                    # suffix text
                    if "suffixtext" not in dict_from_file.keys():
                        dict_from_file["suffixtext"] = False

                    # Special case replies
                    if "specialcase" not in dict_from_file.keys():
                        dict_from_file["specialcase"] = {}
                    if not isinstance(dict_from_file["specialcase"], dict):
                        dict_from_file["specialcase"] = {}
                    for speckey in dict_from_file["specialcase"].keys():
                        if not isinstance(dict_from_file["specialcase"][speckey], dict):
                            dict_from_file["specialcase"][speckey] = {}
                        if "replies" not in dict_from_file["specialcase"][speckey].keys():
                            dict_from_file["specialcase"][speckey]["replies"] = []
                        if not isinstance(dict_from_file["specialcase"][speckey]["replies"], list):
                            if dict_from_file["specialcase"][speckey]["replies"] in bot.memory["botdict"]["tempvals"]['txt_files'].keys():
                                dict_from_file["specialcase"][speckey]["replies"] = bot.memory["botdict"]["tempvals"]['txt_files'][dict_from_file["specialcase"][speckey]["replies"]]
                            elif str(dict_from_file["specialcase"][speckey]["replies"]).startswith(tuple(["https://", "http://"])):
                                page = requests.get(dict_from_file["specialcase"][speckey]["replies"], headers=header)
                                tree = html.fromstring(page.content)
                                if page.status_code == 200:
                                    htmlfile = urllib.urlopen(dict_from_file["specialcase"][speckey]["replies"])
                                    lines = htmlfile.read().splitlines()
                                    dict_from_file["specialcase"][speckey]["replies"] = lines
                            else:
                                dict_from_file["specialcase"][speckey]["replies"] = [dict_from_file["specialcase"][speckey]["replies"]]
                        if "inputrequired" not in dict_from_file["specialcase"][speckey].keys():
                            dict_from_file["specialcase"][speckey]["inputrequired"] = True
                        if "prefixtext" not in dict_from_file["specialcase"][speckey].keys():
                            dict_from_file["specialcase"][speckey]["prefixtext"] = False
                        if "suffixtext" not in dict_from_file["specialcase"][speckey].keys():
                            dict_from_file["specialcase"][speckey]["suffixtext"] = False
                        if "updates_enabled" not in dict_from_file["specialcase"][speckey].keys():
                            dict_from_file["specialcase"][speckey]["updates_enabled"] = False
                        if dict_from_file["specialcase"][speckey]["updates_enabled"]:
                            adjust_nick_array(bot, str(bot.nick), maincom + "_" + str(speckey), dict_from_file["specialcase"][speckey]["replies"], 'startup', 'long', 'sayings')

                    bot.memory["botdict"]["tempvals"]['dict_commands'][maincom] = dict_from_file
                    for comalias in comaliases:
                        if comalias not in bot.memory["botdict"]["tempvals"]['dict_commands'].keys():
                            bot.memory["botdict"]["tempvals"]['dict_commands'][comalias] = {"aliasfor": maincom}


def bot_dictcom_run(bot, trigger):

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
    if botcom.dotcommand not in bot.memory["botdict"]["tempvals"]['dict_commands'].keys():
        return

    # command aliases
    if "aliasfor" in bot.memory["botdict"]["tempvals"]['dict_commands'][botcom.dotcommand]:
        botcom.dotcommand = bot.memory["botdict"]["tempvals"]['dict_commands'][botcom.dotcommand]["aliasfor"]

    # simplify usage of the bot command going forward
    botcom.dotcommand_dict = bot.memory["botdict"]["tempvals"]['dict_commands'][botcom.dotcommand].copy()

    # remainder, if any is the new arg list
    botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+')

    # patch for people typing "...", maybe other stuff, but this verifies that there is still a command here
    if not botcom.dotcommand:
        return

    # execute function based on command type
    botcom.commandtype = botcom.dotcommand_dict["type"].lower()

    # IF "&&" is in the full input, it is treated as multiple commands, and is split
    commands_array = spicemanip(bot, botcom.triggerargsarray, "split_&&")
    if commands_array == []:
        commands_array = [[]]
    for command_split_partial in commands_array:
        botcom.triggerargsarray = spicemanip(bot, command_split_partial, 'create')

        # handling for special cases
        posscom = spicemanip(bot, botcom.triggerargsarray, 1)
        botcom.specialcase = False
        if "specialcase" in botcom.dotcommand_dict.keys():
            if posscom.lower() in botcom.dotcommand_dict["specialcase"].keys():
                botcom.dotcommand_dict["replies"] = botcom.dotcommand_dict["specialcase"][posscom.lower()]["replies"]
                botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+', 'list')
                botcom.specialcase = posscom.lower()

        # This allows users to specify which reply by number by using an ! and a digit (first or last in string)
        botcom.specified = None
        argone, argtwo = spicemanip(bot, botcom.triggerargsarray, 1), spicemanip(bot, botcom.triggerargsarray, 'last')
        if str(argone).startswith("!") and len(str(argone)) > 1:
            if str(argone[1:]).isdigit() or str(argone[1:]) in ['last', 'random', 'count', 'view', 'add', 'del', 'remove']:
                botcom.specified = argone[1:]
            else:
                try:
                    botcom.specified = w2n.word_to_num(str(argone[1:]))
                except ValueError:
                    botcom.specified = None
            if botcom.specified:
                botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+', 'list')
        elif str(argtwo).startswith("!") and len(str(argtwo)) > 1:
            if str(argtwo[1:]).isdigit() or str(argtwo[1:]) in ['last', 'random', 'count', 'view', 'add', 'del', 'remove']:
                botcom.specified = argtwo[1:]
            else:
                try:
                    botcom.specified = w2n.word_to_num(str(argtwo[1:]))
                except ValueError:
                    botcom.specified = None
            if botcom.specified:
                botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, 'last!', 'list')
        if botcom.specified:
            if str(botcom.specified).isdigit():
                botcom.specified = int(botcom.specified)

        if botcom.specialcase:

            if botcom.dotcommand_dict["specialcase"][botcom.specialcase]["updates_enabled"]:
                botcom.dotcommand_dict["replies"] = get_nick_value(bot, str(bot.nick), botcom.dotcommand_dict["validcoms"][0] + "_" + str(botcom.specialcase or 'normal'), 'long', 'sayings') or []

            if botcom.dotcommand_dict["specialcase"][botcom.specialcase]["prefixtext"]:
                botcom.prefixtext = botcom.dotcommand_dict["specialcase"][botcom.specialcase]["prefixtext"]
            else:
                botcom.prefixtext = ""

            if botcom.dotcommand_dict["specialcase"][botcom.specialcase]["suffixtext"]:
                botcom.suffixtext = botcom.dotcommand_dict["specialcase"][botcom.specialcase]["suffixtext"]
            else:
                botcom.suffixtext = ""
        else:

            if "updates_enabled" in botcom.dotcommand_dict.keys():
                if botcom.dotcommand_dict["updates_enabled"]:
                    botcom.dotcommand_dict["replies"] = get_nick_value(bot, str(bot.nick), botcom.dotcommand_dict["validcoms"][0] + "_" + str(botcom.specialcase or 'normal'), 'long', 'sayings') or []

            if botcom.dotcommand_dict["prefixtext"]:
                botcom.prefixtext = botcom.dotcommand_dict["prefixtext"]
            else:
                botcom.prefixtext = ""

            if botcom.dotcommand_dict["suffixtext"]:
                botcom.suffixtext = botcom.dotcommand_dict["suffixtext"]
            else:
                botcom.suffixtext = ""

        posstarget = spicemanip(bot, botcom.triggerargsarray, 1)
        botcom.target = False
        if posstarget in bot.memory["botdict"]["users"].keys():
            botcom.target = posstarget

        # Hardcoded commands
        if botcom.specified == 'count':
            return osd(bot, botcom.channel_current, 'say', "The " + str(botcom.dotcommand_dict["validcoms"][0]) + " " + str(botcom.specialcase or '') + " command has " + str(len(botcom.dotcommand_dict["replies"])) + " entries.")
        elif botcom.specified == 'view':
            if botcom.dotcommand_dict["replies"] == []:
                return osd(bot, botcom.channel_current, 'say', "The " + str(botcom.dotcommand_dict["validcoms"][0]) + " " + str(botcom.specialcase or '') + " command appears to have no entries!")
            else:
                osd(bot, botcom.instigator, 'notice', "The " + str(botcom.dotcommand_dict["validcoms"][0]) + " " + str(botcom.specialcase or '') + " command contains:")
                listnumb, relist = 1, []
                for item in botcom.dotcommand_dict["replies"]:
                    if listnumb <= 20:
                        relist.append(str("[#" + str(listnumb) + "] " + str(item)))
                    listnumb += 1
                osd(bot, botcom.instigator, 'say', relist)
                if listnumb > 20:
                    osd(bot, botcom.instigator, 'say', "List cut off after the 20th entry to prevent bot lag.")
                return

        elif botcom.specified == 'add':

            if botcom.specialcase:
                if not botcom.dotcommand_dict["specialcase"][botcom.specialcase]["updates_enabled"]:
                    return osd(bot, botcom.channel_current, 'say', "The " + str(botcom.dotcommand_dict["validcoms"][0]) + " " + str(botcom.specialcase or '') + " entry list cannot be updated.")
            else:

                if "updates_enabled" not in botcom.dotcommand_dict.keys():
                    return osd(bot, botcom.channel_current, 'say', "The " + str(botcom.dotcommand_dict["validcoms"][0]) + " " + str(botcom.specialcase or '') + " entry list cannot be updated.")
                if not botcom.dotcommand_dict["updates_enabled"]:
                    return osd(bot, botcom.channel_current, 'say', "The " + str(botcom.dotcommand_dict["validcoms"][0]) + " " + str(botcom.specialcase or '') + " entry list cannot be updated.")

            fulltext = spicemanip(bot, botcom.triggerargsarray, 0)
            if not fulltext:
                return osd(bot, botcom.channel_current, 'say', "What would you like to add to the " + str(botcom.dotcommand_dict["validcoms"][0]) + " " + str(botcom.specialcase or '') + " entry list?")
            if fulltext in botcom.dotcommand_dict["replies"]:
                return osd(bot, botcom.channel_current, 'say', "The following was already in the " + str(botcom.dotcommand_dict["validcoms"][0]) + " " + str(botcom.specialcase or '') + " entry list: '" + str(fulltext) + "'")
            adjust_nick_array(bot, str(bot.nick), botcom.dotcommand_dict["validcoms"][0] + "_" + str(botcom.specialcase or 'normal'), fulltext, botcom.specified, 'long', 'sayings')
            return osd(bot, botcom.channel_current, 'say', "The following was added to the " + str(botcom.dotcommand_dict["validcoms"][0]) + " " + str(botcom.specialcase or '') + " entry list: '" + str(fulltext) + "'")

        elif botcom.specified in ['del', 'remove']:

            if botcom.specialcase:
                if not botcom.dotcommand_dict["specialcase"][botcom.specialcase]["updates_enabled"]:
                    return osd(bot, botcom.channel_current, 'say', "The " + str(botcom.dotcommand_dict["validcoms"][0]) + " " + str(botcom.specialcase or '') + " entry list cannot be updated.")
            else:

                if "updates_enabled" not in botcom.dotcommand_dict.keys():
                    return osd(bot, botcom.channel_current, 'say', "The " + str(botcom.dotcommand_dict["validcoms"][0]) + " " + str(botcom.specialcase or '') + " entry list cannot be updated.")
                if not botcom.dotcommand_dict["updates_enabled"]:
                    return osd(bot, botcom.channel_current, 'say', "The " + str(botcom.dotcommand_dict["validcoms"][0]) + " " + str(botcom.specialcase or '') + " entry list cannot be updated.")

            fulltext = spicemanip(bot, botcom.triggerargsarray, 0)
            if not fulltext:
                return osd(bot, botcom.channel_current, 'say', "What would you like to remove from the " + str(botcom.dotcommand_dict["validcoms"][0]) + " " + str(botcom.specialcase or '') + " entry list?")
            if fulltext not in botcom.dotcommand_dict["replies"]:
                return osd(bot, botcom.channel_current, 'say', "The following was already not in the " + str(botcom.dotcommand_dict["validcoms"][0]) + " " + str(botcom.specialcase or '') + " entry list: '" + str(fulltext) + "'")
            adjust_nick_array(bot, str(bot.nick), botcom.dotcommand_dict["validcoms"][0] + "_" + str(botcom.specialcase or 'normal'), fulltext, botcom.specified, 'long', 'sayings')
            return osd(bot, botcom.channel_current, 'say', "The following was removed from the " + str(botcom.dotcommand_dict["validcoms"][0]) + " " + str(botcom.specialcase or '') + " entry list: '" + str(fulltext) + "'")

        botcom.completestring = spicemanip(bot, botcom.triggerargsarray, 0)

        # Run the command with the given info
        command_function_run = str('bot_dictcom_' + botcom.commandtype + '(bot, botcom)')
        eval(command_function_run)


def bot_dictcom_simple(bot, botcom):

    if botcom.specified:
        if botcom.specified > len(botcom.dotcommand_dict["replies"]):
            botcom.specified = len(botcom.dotcommand_dict["replies"])
        replies = spicemanip(bot, botcom.dotcommand_dict["replies"], botcom.specified, 'return')
    else:
        replies = spicemanip(bot, botcom.dotcommand_dict["replies"], 'random', 'return')

    if not isinstance(replies, list):
        replies = [replies]

    # handling for embedded lists
    for rply in replies:
        if botcom.prefixtext != "":
            rply = botcom.prefixtext + rply
        if botcom.suffixtext != "":
            rply = rply + botcom.suffixtext
        rply = rply.replace("$instigator", botcom.instigator)
        rply = rply.replace("$channel", botcom.channel_current)
        rply = rply.replace("$botnick", bot.nick)
        rply = rply.replace("$input", spicemanip(bot, botcom.triggerargsarray, 0) or botcom.dotcommand_dict["validcoms"][0])
        if rply.startswith("time.sleep"):
            eval(rply)
        elif rply.startswith("*a "):
            rply = rply.replace("*a ", "")
            osd(bot, botcom.channel_current, 'action', rply)
        else:
            osd(bot, botcom.channel_current, 'say', rply)


def bot_dictcom_target(bot, botcom):

    # some commands cannot run without input
    targetrequired, ignoretarget = 1, 0

    if botcom.specialcase:
        if not botcom.dotcommand_dict["specialcase"][botcom.specialcase]["inputrequired"]:
            targetrequired = 0

    if "backuptarget" in botcom.dotcommand_dict.keys() and not botcom.target:
        targetrequired = 0
        botcom.target = botcom.dotcommand_dict["backuptarget"]
        if botcom.target == 'instigator':
            botcom.target = botcom.instigator
        elif botcom.target == 'random':
            if not botcom.channel_current.startswith('#'):
                botcom.target = botcom.instigator
            else:
                botcom.target = spicemanip(bot, bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['current_users'], 'random')
        else:
            ignoretarget = 1

    if "noinputreplies" in botcom.dotcommand_dict.keys() and not botcom.target and targetrequired:
        targetrequired = 0
        botcom.dotcommand_dict["replies"] = botcom.dotcommand_dict["noinputreplies"]

    if botcom.target:
        targetrequired = 0

    if targetrequired:
        return osd(bot, botcom.instigator, 'notice', "This command requires a target.")

    # remove target
    if spicemanip(bot, botcom.triggerargsarray, 1) == botcom.target:
        botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+', 'list')

    if not ignoretarget and botcom.target:
        targetchecking = bot_target_check(bot, botcom, botcom.target)
        if not targetchecking["targetgood"]:
            if targetchecking["reason"] == "bot" and "botreact" in botcom.dotcommand_dict.keys():
                botcom.dotcommand_dict["replies"] = botcom.dotcommand_dict["botreact"]
            else:
                return osd(bot, botcom.instigator, 'notice', targetchecking["error"])

    if botcom.specified:
        if botcom.specified > len(botcom.dotcommand_dict["replies"]):
            botcom.specified = len(botcom.dotcommand_dict["replies"])
        replies = spicemanip(bot, botcom.dotcommand_dict["replies"], botcom.specified, 'return')
    else:
        replies = spicemanip(bot, botcom.dotcommand_dict["replies"], 'random', 'return')

    if not isinstance(replies, list):
        replies = [replies]

    if not botcom.target:
        ignoretarget = 1
        botcom.target = ''

    for rply in replies:
        if botcom.prefixtext != "":
            rply = botcom.prefixtext + rply
        if botcom.suffixtext != "":
            rply = rply + botcom.suffixtext
        rply = rply.replace("$target", botcom.target)
        rply = rply.replace("$instigator", botcom.instigator)
        rply = rply.replace("$channel", botcom.channel_current)
        rply = rply.replace("$botnick", bot.nick)
        rply = rply.replace("$input", spicemanip(bot, botcom.triggerargsarray, 0) or botcom.dotcommand_dict["validcoms"][0])
        if rply.startswith("time.sleep"):
            eval(rply)
        elif rply.startswith("*a "):
            rply = rply.replace("*a ", "")
            osd(bot, botcom.channel_current, 'action', rply)
        else:
            osd(bot, botcom.channel_current, 'say', rply)


def bot_dictcom_fillintheblank(bot, botcom):

    # some commands cannot run without input
    inputrequired = 1

    if botcom.specialcase:
        if not botcom.dotcommand_dict["specialcase"][botcom.specialcase]["inputrequired"]:
            inputrequired = 0

    if "backupblank" in botcom.dotcommand_dict.keys() and not botcom.completestring:
        botcom.completestring = botcom.dotcommand_dict["backupblank"]

    if "noinputreplies" in botcom.dotcommand_dict.keys() and not botcom.completestring and inputrequired:
        inputrequired = 0
        botcom.dotcommand_dict["replies"] = botcom.dotcommand_dict["noinputreplies"]

    if botcom.completestring:
        inputrequired = 0

    if inputrequired:
        return osd(bot, botcom.instigator, 'notice', "This command requires input.")

    if botcom.specified:
        if botcom.specified > len(botcom.dotcommand_dict["replies"]):
            botcom.specified = len(botcom.dotcommand_dict["replies"])
        replies = spicemanip(bot, botcom.dotcommand_dict["replies"], botcom.specified, 'return')
    else:
        replies = spicemanip(bot, botcom.dotcommand_dict["replies"], 'random', 'return')

    # handling for embedded lists
    if not isinstance(replies, list):
        replies = [replies]

    for rply in replies:
        if botcom.prefixtext != "":
            rply = botcom.prefixtext + rply
        if botcom.suffixtext != "":
            rply = rply + botcom.suffixtext
        rply = rply.replace("$blank", botcom.completestring)
        rply = rply.replace("$instigator", botcom.instigator)
        rply = rply.replace("$channel", botcom.channel_current)
        rply = rply.replace("$botnick", bot.nick)
        rply = rply.replace("$input", spicemanip(bot, botcom.triggerargsarray, 0) or botcom.dotcommand_dict["validcoms"][0])
        if rply.startswith("time.sleep"):
            eval(rply)
        elif rply.startswith("*a "):
            rply = rply.replace("*a ", "")
            osd(bot, botcom.channel_current, 'action', rply)
        else:
            osd(bot, botcom.channel_current, 'say', rply)


def bot_dictcom_targetplusreason(bot, botcom):

    # some commands cannot run without input
    targetrequired, ignoretarget = 1, 0

    if botcom.specialcase:
        if not botcom.dotcommand_dict["specialcase"][botcom.specialcase]["inputrequired"]:
            targetrequired = 0

    if "backuptarget" in botcom.dotcommand_dict.keys() and not botcom.target:
        targetrequired = 0
        botcom.target = botcom.dotcommand_dict["backuptarget"]
        if botcom.target == 'instigator':
            botcom.target = botcom.instigator
        elif botcom.target == 'random':
            if not botcom.channel_current.startswith('#'):
                botcom.target = botcom.instigator
            else:
                botcom.target = spicemanip(bot, bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['current_users'], 'random')
        else:
            ignoretarget = 1

    if "noinputreplies" in botcom.dotcommand_dict.keys() and not botcom.target and targetrequired:
        targetrequired = 0
        botcom.dotcommand_dict["replies"] = botcom.dotcommand_dict["noinputreplies"]

    if botcom.target:
        targetrequired = 0

    if targetrequired:
        return osd(bot, botcom.instigator, 'notice', "This command requires a target.")

    # remove target
    if spicemanip(bot, botcom.triggerargsarray, 1) == botcom.target:
        botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+', 'list')
    botcom.completestring = spicemanip(bot, botcom.triggerargsarray, 0)

    # some commands cannot run without input
    inputrequired, ignorefillin = 1, 0

    if "backupblank" in botcom.dotcommand_dict.keys() and not botcom.completestring:
        botcom.completestring = botcom.dotcommand_dict["backupblank"]
        ignorefillin = 1

    if botcom.completestring:
        inputrequired = 0

    if inputrequired:
        return osd(bot, botcom.instigator, 'notice', "This command requires input.")

    if not ignoretarget and botcom.target:
        targetchecking = bot_target_check(bot, botcom, botcom.target)
        if not targetchecking["targetgood"]:
            if targetchecking["reason"] == "bot" and "botreact" in botcom.dotcommand_dict.keys():
                botcom.dotcommand_dict["replies"] = botcom.dotcommand_dict["botreact"]
            else:
                return osd(bot, botcom.instigator, 'notice', targetchecking["error"])

    if botcom.specified:
        if botcom.specified > len(botcom.dotcommand_dict["replies"]):
            botcom.specified = len(botcom.dotcommand_dict["replies"])
        replies = spicemanip(bot, botcom.dotcommand_dict["replies"], botcom.specified, 'return')
    else:
        replies = spicemanip(bot, botcom.dotcommand_dict["replies"], 'random', 'return')

    if "reasonhandle" in botcom.dotcommand_dict.keys():
        if spicemanip(bot, botcom.completestring, 1).lower() not in botcom.dotcommand_dict["reasonhandle"] and not ignorefillin:
            botcom.completestring = botcom.dotcommand_dict["reasonhandle"][0] + " " + botcom.completestring
        elif spicemanip(bot, botcom.completestring, 1).lower() in botcom.dotcommand_dict["reasonhandle"] and not ignorefillin:
            if spicemanip(bot, botcom.completestring, 1).lower() != botcom.dotcommand_dict["reasonhandle"][0]:
                botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+', 'list')
                if botcom.triggerargsarray != []:
                    botcom.completestring = botcom.dotcommand_dict["reasonhandle"][0] + " " + spicemanip(bot, botcom.triggerargsarray, 0)

    if not isinstance(replies, list):
        replies = [replies]

    if not botcom.target:
        ignoretarget = 1
        botcom.target = ''

    for rply in replies:
        if botcom.prefixtext != "":
            rply = botcom.prefixtext + rply
        if botcom.suffixtext != "":
            rply = rply + botcom.suffixtext
        rply = rply.replace("$blank", botcom.completestring)
        rply = rply.replace("$target", botcom.target)
        rply = rply.replace("$instigator", botcom.instigator)
        rply = rply.replace("$channel", botcom.channel_current)
        rply = rply.replace("$botnick", bot.nick)
        rply = rply.replace("$input", spicemanip(bot, botcom.triggerargsarray, 0) or botcom.dotcommand_dict["validcoms"][0])
        if rply.startswith("time.sleep"):
            eval(rply)
        elif rply.startswith("*a "):
            rply = rply.replace("*a ", "")
            osd(bot, botcom.channel_current, 'action', rply)
        else:
            osd(bot, botcom.channel_current, 'say', rply)


def bot_dictcom_gif(bot, botcom):

    if "query" in botcom.dotcommand_dict.keys():
        query = botcom.dotcommand_dict["query"]
    else:
        query = botcom.completestring

    if botcom.dotcommand in bot.memory["botdict"]["tempvals"]['valid_gif_api_dict'].keys():
        searchapis = [botcom.dotcommand]
    elif "queryapi" in botcom.dotcommand_dict.keys():
        searchapis = botcom.dotcommand_dict["queryapi"]
    else:
        searchapis = bot.memory["botdict"]["tempvals"]['valid_gif_api_dict'].keys()

    searchdict = {"query": query, "gifsearch": searchapis}

    if botcom.specified:
        searchdict["pickingselection"] = botcom.specified

    # nsfwenabled = get_database_value(bot, bot.nick, 'channels_nsfw') or []
    # if botcom.channel_current in nsfwenabled:
    #    searchdict['nsfw'] = True

    gifdict = getGif(bot, searchdict)

    if gifdict["error"]:
        if "noinputreplies" in botcom.dotcommand_dict.keys():
            botcom.dotcommand_dict["replies"] = botcom.dotcommand_dict["noinputreplies"]
            if botcom.specified:
                if botcom.specified > len(botcom.dotcommand_dict["replies"]):
                    botcom.specified = len(botcom.dotcommand_dict["replies"])
                replies = spicemanip(bot, botcom.dotcommand_dict["replies"], botcom.specified, 'return')
            else:
                replies = spicemanip(bot, botcom.dotcommand_dict["replies"], 'random', 'return')

            if not isinstance(replies, list):
                replies = [replies]
            # handling for embedded lists
            for rply in replies:
                if botcom.prefixtext != "":
                    rply = botcom.prefixtext + rply
                if botcom.suffixtext != "":
                    rply = rply + botcom.suffixtext
                rply = rply.replace("$instigator", botcom.instigator)
                rply = rply.replace("$channel", botcom.channel_current)
                rply = rply.replace("$botnick", bot.nick)
                rply = rply.replace("$input", spicemanip(bot, botcom.triggerargsarray, 0) or botcom.dotcommand_dict["validcoms"][0])
                if rply.startswith("time.sleep"):
                    eval(rply)
                elif rply.startswith("*a "):
                    rply = rply.replace("*a ", "")
                    osd(bot, botcom.channel_current, 'action', rply)
                else:
                    osd(bot, botcom.channel_current, 'say', rply)
        else:
            osd(bot, botcom.channel_current, 'say',  str(gifdict["error"]))
        return

    osd(bot, botcom.channel_current, 'say',  gifdict['gifapi'].title() + " Result (" + str(query) + " #" + str(gifdict["returnnum"]) + "): " + str(gifdict["returnurl"]))


def bot_dictcom_ascii_art(bot, botcom):
    return bot_dictcom_simple(bot, botcom)


def bot_dictcom_sayings(bot, botcom):
    return bot_dictcom_simple(bot, botcom)


def bot_dictcom_readfromurl(bot, botcom):
    return bot_dictcom_simple(bot, botcom)


def bot_dictcom_readfromfile(bot, botcom):
    return bot_dictcom_simple(bot, botcom)


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
                    "pickingselection": "random",
                    }

    # set defaults if they don't exist
    for key in query_defaults:
        if key not in searchdict.keys():
            searchdict[key] = query_defaults[key]
            if key == "gifsearch":
                for remx in query_defaults["gifsearchremove"]:
                    searchdict["gifsearch"].remove(remx)

    # Replace spaces in search query
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
                    tempdict = dict()
                    tempdict["returnnum"] = tempresultnum
                    tempdict["returnurl"] = tempresult
                    tempdict["gifapi"] = currentapi
                    tempresultnum += 1
                    gifapiresults.append(tempdict)

    if gifapiresults == []:
        return {"error": "No Results were found for '" + searchdict["query"] + "' in the " + str(spicemanip(bot, searchdict['gifsearch'], 'orlist')) + " api(s)"}

    random.shuffle(gifapiresults)
    random.shuffle(gifapiresults)
    if searchdict["pickingselection"] not in ["random", "last"]:
        if searchdict["pickingselection"] > len(gifapiresults):
            searchdict["pickingselection"] = len(gifapiresults)
    gifdict = spicemanip(bot, gifapiresults, searchdict["pickingselection"])

    # return dict
    gifdict['error'] = None
    return gifdict


"""
Bot Servers
"""


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


def ipv4detect(bot, hostIP):
    pat = re.compile("\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}")
    test = pat.match(hostIP)
    return test


"""
Bot Channels
"""


def botdict_setup_channels(bot):

    # All channels the bot is in
    if bot.memory["botdict"]["tempvals"]['channels_list'].keys() == []:
        for channel in bot.channels:
            if channel not in bot.memory["botdict"]["tempvals"]['channels_list'].keys():
                bot.memory["botdict"]["tempvals"]['channels_list'][channel] = dict()


"""
Bots
"""


def botdict_setup_bots(bot):

    if bot.memory["botdict"]["tempvals"]['bot_admins'] == []:
        bot.memory["botdict"]["tempvals"]['bot_admins'] = bot.config.core.admins

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


"""
Users
"""


def botdict_setup_users(bot):

    for channelcheck in bot.memory["botdict"]["tempvals"]['channels_list'].keys():

        if 'chanops' not in bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck].keys():
            bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck]['chanops'] = []

        if 'chanhalfops' not in bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck].keys():
            bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck]['chanhalfops'] = []

        if 'chanvoices' not in bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck].keys():
            bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck]['chanvoices'] = []

        if 'current_users' not in bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck].keys():
            bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck]['current_users'] = []

        userprivdict = {}
        for user in bot.privileges[channelcheck].keys():
            if user not in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
                if user not in bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck]['current_users']:
                    bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck]['current_users'].append(user)
                userprivdict[user] = bot.privileges[channelcheck][user] or 0

        for user in bot.memory["botdict"]["tempvals"]['channels_list'][channelcheck]['current_users']:
            if user in userprivdict.keys():

                for privtype in ['VOICE', 'HALFOP', 'OP']:
                    privstring = str("chan" + privtype.lower() + "s")
                    if userprivdict[user] == eval(privtype):
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


def bot_target_check(bot, botcom, target):
    targetgood = {"targetgood": True, "error": "None", "reason": None}

    targetgoodconsensus, reasons = [], []

    # cannot target bots
    if target in bot.memory["botdict"]["tempvals"]['bots_list']:
        reasons.append("bot")
        targetgoodconsensus.append(nick_actual(bot, target) + " is a bot and cannot be targeted.")

    # Not a valid user
    if target not in bot.memory["botdict"]["users"].keys():
        reasons.append("unknown")
        targetgoodconsensus.append("I don't know who that is.")

    # User offline
    if target not in bot.memory["botdict"]["tempvals"]['all_current_users']:
        reasons.append("offline")
        targetgoodconsensus.append("It looks like " + nick_actual(bot, target) + " is offline right now!")

    if not botcom.channel_current.startswith('#') and target != botcom.instigator:
        reasons.append("privmsg")
        targetgoodconsensus.append("Leave " + nick_actual(bot, target) + " out of this private conversation!")

    if target in bot.memory["botdict"]["tempvals"]['all_current_users'] and target not in bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['current_users']:
        reasons.append("diffchannel")
        targetgoodconsensus.append("It looks like " + nick_actual(bot, target) + " is online right now, but in a different channel.")

    if targetgoodconsensus != []:
        targetgood = {"targetgood": False, "error": targetgoodconsensus[0], "reason": reasons[0]}

    return targetgood


def bot_watch_part_run(bot, trigger):

    # botcom dynamic Class
    botcom = class_create('botcom')
    botcom.default = 'botcom'

    # instigator
    botcom.instigator = trigger.nick

    # channel
    botcom.channel_current = trigger.sender

    # database entry for user
    if botcom.instigator not in bot.memory["botdict"]["users"].keys():
        bot.memory["botdict"]["users"][botcom.instigator] = dict()

    # channel list
    if botcom.instigator in bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['current_users']:
        bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['current_users'].remove(botcom.instigator)

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


def bot_watch_kick_run(bot, trigger):

    # botcom dynamic Class
    botcom = class_create('botcom')
    botcom.default = 'botcom'

    # instigator
    botcom.instigator = trigger.nick

    # channel
    botcom.channel_current = trigger.sender

    # target user
    botcom.target = trigger.args[1]

    # database entry for user
    if botcom.target not in bot.memory["botdict"]["users"].keys():
        bot.memory["botdict"]["users"][botcom.target] = dict()

    # channel list
    if botcom.target in bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['current_users']:
        bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['current_users'].remove(botcom.target)

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


def bot_watch_quit_run(bot, trigger):

    # botcom dynamic Class
    botcom = class_create('botcom')
    botcom.default = 'botcom'

    # instigator
    botcom.instigator = trigger.nick

    # channel
    botcom.channel_current = trigger.sender

    # database entry for user
    if botcom.instigator not in bot.memory["botdict"]["users"].keys():
        bot.memory["botdict"]["users"][botcom.instigator] = dict()

    # channel list
    for channel in bot.memory["botdict"]["tempvals"]['channels_list'].keys():
        if botcom.instigator in bot.memory["botdict"]["tempvals"]['channels_list'][channel]['current_users']:
            bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['current_users'].remove(botcom.instigator)

    if botcom.instigator not in bot.memory["botdict"]["tempvals"]['bots_list'].keys():
        if botcom.instigator not in bot.memory["botdict"]["tempvals"]['offline_users']:
            bot.memory["botdict"]["tempvals"]['offline_users'].append(botcom.instigator)

    if botcom.instigator in bot.memory["botdict"]["tempvals"]['all_current_users']:
        bot.memory["botdict"]["tempvals"]['all_current_users'].remove(botcom.instigator)


def bot_watch_join_run(bot, trigger):

    # botcom dynamic Class
    botcom = class_create('botcom')
    botcom.default = 'botcom'

    # instigator
    botcom.instigator = trigger.nick

    # channel
    botcom.channel_current = trigger.sender

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

    # remove from offline
    if botcom.instigator in bot.memory["botdict"]["tempvals"]['offline_users']:
        bot.memory["botdict"]["tempvals"]['offline_users'].remove(botcom.instigator)


def bot_watch_mode_run(bot, trigger):

    global mode_dict_alias

    # botcom dynamic Class
    botcom = class_create('botcom')
    botcom.default = 'botcom'

    # instigator
    botcom.instigator = trigger.nick

    # channel
    botcom.channel_current = trigger.sender

    # target
    target = trigger.args[-1]

    # Mode set
    modeused = trigger.args[1]

    if str(modeused).startswith("-"):
        modetype = 'del'
    elif str(modeused).startswith("+"):
        modetype = 'add'

    if modeused[1:] in mode_dict_alias.keys():

        userprivdict = {}
        userprivdict[target] = eval(mode_dict_alias[modeused[1:]])

        for privtype in ['VOICE', 'HALFOP', 'OP']:
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
                    if target not in bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current][privstring]:
                        bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current][privstring].append(target)


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


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def countX(lst, x):
    count = 0
    for ele in lst:
        if (ele == x):
            count = count + 1
    return count


"""
Botdict Nick values
"""


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
