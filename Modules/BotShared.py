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

# Opening and reading config files
import ConfigParser


# Ensure Encoding
reload(sys)
sys.setdefaultencoding('utf-8')

"""
Variables # TODO add to botdict
"""


osd_limit = 420  # Ammount of text allowed to display per line

valid_com_types = ['simple', 'target', 'fillintheblank', 'targetplusblank', 'sayings', "readfromfile"]


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

"""
Dict functions
"""


def botdict_open(bot):

    if "botdict_loaded" in bot.memory:
        return

    bot.memory["botdict"] = botdict_setup_open(bot)

    if not bot.memory["botdict"]["tempvals"]["uptime"]:
        bot.memory["botdict"]["tempvals"]["uptime"] = datetime.datetime.utcnow()

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
Testing
"""


def bot_command_function_dict(bot, botcom):
    osd(bot, botcom.channel_current, 'say', str(bot.memory["botdict"]["users"]))


"""
Dictionary commands
"""


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
            bot.msg("#spicebottest", str(len(bot.memory["botdict"]["tempvals"]['txt_files'][txtfile])))


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
                inf = open(os.path.join(coms_type_file_path, comconf), 'r')
                try:
                    dict_from_file = eval(inf.read())
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
                        dict_from_file["reply"] = "This command is not setup with a proper 'type'."

                    # check that reply is set
                    if "reply" not in dict_from_file.keys():
                        dict_from_file["reply"] = "Reply missing"
                    if dict_from_file["type"] == 'sayings' and dict_from_file["reply"] != "Reply missing":
                        adjust_nick_array(bot, str(bot.nick), maincom, dict_from_file["reply"], 'startup', 'long', 'sayings')
                    if dict_from_file["type"] == 'readfromfile':
                        dict_from_file["type"] = 'simple'
                        if "filename" in dict_from_file.keys():
                            if dict_from_file["filename"] in bot.memory["botdict"]["tempvals"]['txt_files'].keys():
                                dict_from_file["reply"] = bot.memory["botdict"]["tempvals"]['txt_files'][dict_from_file["filename"]]

                    # make replies in list form if not
                    if not isinstance(dict_from_file["reply"], list):
                        dict_from_file["reply"] = [dict_from_file["reply"]]
                    if "noinputreply" in dict_from_file.keys():
                        if not isinstance(dict_from_file["noinputreply"], list):
                            dict_from_file["noinputreply"] = [dict_from_file["noinputreply"]]

                    if "reasonhandle" in dict_from_file.keys():
                        if not isinstance(dict_from_file["reasonhandle"], list):
                            dict_from_file["reasonhandle"] = [dict_from_file["reasonhandle"]]

                    if "specialcase" not in dict_from_file.keys():
                        dict_from_file["specialcase"] = {}
                    for speckey in dict_from_file["specialcase"].keys():
                        if not isinstance(dict_from_file["specialcase"][speckey], list):
                            dict_from_file["specialcase"][speckey] = [dict_from_file["specialcase"][speckey]]

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
    botcom.dotcommand_dict = bot.memory["botdict"]["tempvals"]['dict_commands'][botcom.dotcommand]

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

        # This allows users to specify which reply by number by using an ! and a digit (first or last in string)
        botcom.specified = None
        argone, argtwo = spicemanip(bot, botcom.triggerargsarray, 1), spicemanip(bot, botcom.triggerargsarray, 'last')
        if str(argone).startswith("!") and len(str(argone)) > 1:
            if str(argone[1:]).isdigit() or str(argone[1:]) in ['last', 'random']:
                botcom.specified = argone[1:]
                if str(botcom.specified).isdigit():
                    botcom.specified = int(botcom.specified)
                botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+', 'list')
        elif str(argtwo).startswith("!") and len(str(argtwo)) > 1:
            if str(argtwo[1:]).isdigit() or str(argtwo[1:]) in ['last', 'random']:
                botcom.specified = argtwo[1:]
                if str(botcom.specified).isdigit():
                    botcom.specified = int(botcom.specified)
                botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, 'last!', 'list')

        # Run the command with the given info
        command_function_run = str('bot_dictcom_' + botcom.commandtype + '(bot, botcom)')
        eval(command_function_run)


def bot_dictcom_simple(bot, botcom):

    posscom = spicemanip(bot, botcom.triggerargsarray, 1)
    if "specialcase" in botcom.dotcommand_dict.keys():
        if posscom.lower() in botcom.dotcommand_dict["specialcase"].keys():
            botcom.dotcommand_dict["reply"] = botcom.dotcommand_dict["specialcase"][posscom.lower()]

    if botcom.specified:
        if botcom.specified > len(botcom.dotcommand_dict["reply"]):
            botcom.specified = len(botcom.dotcommand_dict["reply"])
        reply = spicemanip(bot, botcom.dotcommand_dict["reply"], botcom.specified, 'return')
    else:
        reply = spicemanip(bot, botcom.dotcommand_dict["reply"], 'random', 'return')

    if not isinstance(reply, list):
        reply = [reply]

    for rply in reply:
        rply = rply.replace("$instigator", botcom.instigator)
        rply = rply.replace("$channel", botcom.channel_current)
        if rply.startswith("time.sleep"):
            eval(rply)
        elif rply.startswith("*a "):
            rply = rply.replace("*a ", "")
            osd(bot, botcom.channel_current, 'action', rply)
        else:
            osd(bot, botcom.channel_current, 'say', rply)


def bot_dictcom_sayings(bot, botcom):

    command = spicemanip(bot, botcom.triggerargsarray, 1) or 'get'
    # remove command
    if command in botcom.triggerargsarray:
        botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+', 'list')
    aftercom = spicemanip(bot, botcom.triggerargsarray, 0)

    botcom.dotcommand_dict["reply"] = get_nick_value(bot, str(bot.nick), botcom.dotcommand_dict["validcoms"][0], 'long', 'sayings') or []

    if "specialcase" in botcom.dotcommand_dict.keys():
        if command.lower() in botcom.dotcommand_dict["specialcase"].keys():
            botcom.dotcommand_dict["reply"] = botcom.dotcommand_dict["specialcase"][command.lower()]
            command = 'get'

    if command == 'add':
        if not aftercom:
            return osd(bot, botcom.channel_current, 'say', "What would you like to add to the " + str(botcom.dotcommand_dict["validcoms"][0]) + " database?")
        if aftercom in botcom.dotcommand_dict["reply"]:
            return osd(bot, botcom.channel_current, 'say', "The following was already in the " + str(botcom.dotcommand_dict["validcoms"][0]) + " database: '" + str(aftercom) + "'")
        adjust_nick_array(bot, str(bot.nick), botcom.dotcommand_dict["validcoms"][0], aftercom, command, 'long', 'sayings')
        return osd(bot, botcom.channel_current, 'say', "The following was added to the " + str(botcom.dotcommand_dict["validcoms"][0]) + " database: '" + str(aftercom) + "'")

    elif command in ['del', 'remove']:
        if not aftercom:
            return osd(bot, botcom.channel_current, 'say', "What would you like to remove from the " + str(botcom.dotcommand_dict["validcoms"][0]) + " database?")
        if aftercom not in botcom.dotcommand_dict["reply"]:
            return osd(bot, botcom.channel_current, 'say', "The following was already not in the " + str(botcom.dotcommand_dict["validcoms"][0]) + " database: '" + str(aftercom) + "'")
        adjust_nick_array(bot, str(bot.nick), botcom.dotcommand_dict["validcoms"][0], aftercom, command, 'long', 'sayings')
        return osd(bot, botcom.channel_current, 'say', "The following was removed from the " + str(botcom.dotcommand_dict["validcoms"][0]) + " database: '" + str(aftercom) + "'")

    elif command == 'count':
        return osd(bot, botcom.channel_current, 'say', "The " + str(botcom.dotcommand_dict["validcoms"][0]) + " database has " + str(len(botcom.dotcommand_dict["reply"])) + " entries.")

    elif command == 'view':
        if botcom.dotcommand_dict["reply"] == []:
            return osd(bot, botcom.channel_current, 'say', "The " + str(botcom.dotcommand_dict["validcoms"][0]) + " database appears to be empty!")
        else:
            osd(bot, botcom.instigator, 'notice', "The " + str(botcom.dotcommand_dict["validcoms"][0]) + "contains:")
            osd(bot, botcom.instigator, 'say', botcom.dotcommand_dict["reply"])
            return

    elif command == 'get':

        if botcom.dotcommand_dict["reply"] == []:
            return osd(bot, botcom.channel_current, 'say', "The " + str(botcom.dotcommand_dict["validcoms"][0]) + " database appears to be empty!")

        if botcom.specified:
            if botcom.specified > len(botcom.dotcommand_dict["reply"]):
                botcom.specified = len(botcom.dotcommand_dict["reply"])
            reply = spicemanip(bot, botcom.dotcommand_dict["reply"], botcom.specified, 'return')
        else:
            reply = spicemanip(bot, botcom.dotcommand_dict["reply"], 'random', 'return')

        if not isinstance(reply, list):
            reply = [reply]

        for rply in reply:
            rply = rply.replace("$instigator", botcom.instigator)
            rply = rply.replace("$channel", botcom.channel_current)
            if rply.startswith("time.sleep"):
                eval(rply)
            elif rply.startswith("*a "):
                rply = rply.replace("*a ", "")
                osd(bot, botcom.channel_current, 'action', rply)
            else:
                osd(bot, botcom.channel_current, 'say', rply)


def bot_dictcom_target(bot, botcom):

    # target is the first arg given
    target = spicemanip(bot, botcom.triggerargsarray, 1)
    ignoretarget = False

    if target not in bot.memory["botdict"]["users"].keys() and "specialcase" in botcom.dotcommand_dict.keys() and not ignoretarget:
        if target.lower() in botcom.dotcommand_dict["specialcase"].keys():
            ignoretarget = True
            botcom.dotcommand_dict["reply"] = botcom.dotcommand_dict["specialcase"][target.lower()]
            target = ''

    # handling for no target
    if target not in bot.memory["botdict"]["users"].keys() and "noinputreply" in botcom.dotcommand_dict.keys():
        target = ''
        ignoretarget = True
        botcom.dotcommand_dict["reply"] = botcom.dotcommand_dict["noinputreply"]

    if target not in bot.memory["botdict"]["users"].keys() and "backuptarget" in botcom.dotcommand_dict.keys() and not ignoretarget:
        target = botcom.dotcommand_dict["backuptarget"]
        ignoretarget = True
        if target == 'instigator':
            target = botcom.instigator
        elif target == 'random':
            if not botcom.channel_current.startswith('#'):
                target = botcom.instigator
            else:
                target = spicemanip(bot, bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['current_users'], 'random')

    if target not in bot.memory["botdict"]["users"].keys() and not ignoretarget:
        return osd(bot, botcom.instigator, 'notice', "This command requires a target.")

    if botcom.specified:
        if botcom.specified > len(botcom.dotcommand_dict["reply"]):
            botcom.specified = len(botcom.dotcommand_dict["reply"])
        reply = spicemanip(bot, botcom.dotcommand_dict["reply"], botcom.specified, 'return')
    else:
        reply = spicemanip(bot, botcom.dotcommand_dict["reply"], 'random', 'return')

    # remove target
    if target in botcom.triggerargsarray:
        botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+', 'list')

    if not ignoretarget:
        targetchecking = bot_target_check(bot, botcom, target)
        if not targetchecking["targetgood"]:
            return osd(bot, botcom.instigator, 'notice', targetchecking["error"])

    if not isinstance(reply, list):
        reply = [reply]

    for rply in reply:
        rply = rply.replace("$target", target)
        rply = rply.replace("$instigator", botcom.instigator)
        rply = rply.replace("$channel", botcom.channel_current)
        if rply.startswith("time.sleep"):
            eval(rply)
        elif rply.startswith("*a "):
            rply = rply.replace("*a ", "")
            osd(bot, botcom.channel_current, 'action', rply)
        else:
            osd(bot, botcom.channel_current, 'say', rply)


def bot_dictcom_fillintheblank(bot, botcom):

    # all text given is valid for use
    fillin = spicemanip(bot, botcom.triggerargsarray, 0)
    ignorefillin = False

    posscom = spicemanip(bot, botcom.triggerargsarray, 1)
    if "specialcase" in botcom.dotcommand_dict.keys():
        if posscom.lower() in botcom.dotcommand_dict["specialcase"].keys():
            botcom.dotcommand_dict["reply"] = botcom.dotcommand_dict["specialcase"][posscom.lower()]

    # handling for no fillin
    if not fillin and "noinputreply" in botcom.dotcommand_dict.keys() and not ignorefillin:
        botcom.dotcommand_dict["reply"] = botcom.dotcommand_dict["noinputreply"]
        ignorefillin = True

    if not fillin and "backupblank" in botcom.dotcommand_dict.keys():
        fillin = botcom.dotcommand_dict["backupblank"]
        ignorefillin = True

    if not fillin and not ignorefillin:
        return osd(bot, botcom.instigator, 'notice', "This command requires input.")

    if botcom.specified:
        if botcom.specified > len(botcom.dotcommand_dict["reply"]):
            botcom.specified = len(botcom.dotcommand_dict["reply"])
        reply = spicemanip(bot, botcom.dotcommand_dict["reply"], botcom.specified, 'return')
    else:
        reply = spicemanip(bot, botcom.dotcommand_dict["reply"], 'random', 'return')

    if "reasonhandle" in botcom.dotcommand_dict.keys():
        if spicemanip(bot, fillin, 1).lower() not in botcom.dotcommand_dict["reasonhandle"] and not ignorefillin:
            fillin = botcom.dotcommand_dict["reasonhandle"][0] + " " + fillin
        elif spicemanip(bot, fillin, 1).lower() in botcom.dotcommand_dict["reasonhandle"] and not ignorefillin:
            if spicemanip(bot, fillin, 1).lower() != botcom.dotcommand_dict["reasonhandle"][0]:
                botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+', 'list')
                fillin = botcom.dotcommand_dict["reasonhandle"][0] + " " + spicemanip(bot, botcom.triggerargsarray, 0)

    if not isinstance(reply, list):
        reply = [reply]

    for rply in reply:
        rply = rply.replace("$blank", fillin)
        rply = rply.replace("$instigator", botcom.instigator)
        rply = rply.replace("$channel", botcom.channel_current)
        if rply.startswith("time.sleep"):
            eval(rply)
        elif rply.startswith("*a "):
            rply = rply.replace("*a ", "")
            osd(bot, botcom.channel_current, 'action', rply)
        else:
            osd(bot, botcom.channel_current, 'say', rply)


def bot_dictcom_targetplusblank(bot, botcom):

    ignorefillin = False
    ignoretarget = False

    # target is the first arg given
    target = spicemanip(bot, botcom.triggerargsarray, 1)

    if target not in bot.memory["botdict"]["users"].keys() and "specialcase" in botcom.dotcommand_dict.keys() and not ignoretarget:
        if target.lower() in botcom.dotcommand_dict["specialcase"].keys():
            ignoretarget = True
            botcom.dotcommand_dict["reply"] = botcom.dotcommand_dict["specialcase"][target.lower()]
            target = ''

    if target not in bot.memory["botdict"]["users"].keys() and "backuptarget" in botcom.dotcommand_dict.keys() and not ignoretarget:
        target = botcom.dotcommand_dict["backuptarget"]
        ignoretarget = True
        if target == 'instigator':
            target = botcom.instigator
        elif target == 'random':
            if not botcom.channel_current.startswith('#'):
                target = botcom.instigator
            else:
                target = spicemanip(bot, bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['current_users'], 'random')
    if target not in bot.memory["botdict"]["users"].keys() and not ignoretarget:
        return osd(bot, botcom.instigator, 'notice', "This command requires a target.")

    if not ignoretarget:
        targetchecking = bot_target_check(bot, botcom, target)
        if not targetchecking["targetgood"]:
            return osd(bot, botcom.instigator, 'notice', targetchecking["error"])

    # remove target
    if target in botcom.triggerargsarray:
        botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+', 'list')

    # all text given is valid for use
    fillin = spicemanip(bot, botcom.triggerargsarray, 0)

    if not fillin and "backupblank" in botcom.dotcommand_dict.keys():
        fillin = botcom.dotcommand_dict["backupblank"]
        ignorefillin = True
    if not fillin and not ignorefillin:
        return osd(bot, botcom.instigator, 'notice', "This command requires input.")

    if botcom.specified:
        if botcom.specified > len(botcom.dotcommand_dict["reply"]):
            botcom.specified = len(botcom.dotcommand_dict["reply"])
        reply = spicemanip(bot, botcom.dotcommand_dict["reply"], botcom.specified, 'return')
    else:
        reply = spicemanip(bot, botcom.dotcommand_dict["reply"], 'random', 'return')

    if "reasonhandle" in botcom.dotcommand_dict.keys():
        if spicemanip(bot, fillin, 1).lower() not in botcom.dotcommand_dict["reasonhandle"] and not ignorefillin:
            fillin = botcom.dotcommand_dict["reasonhandle"][0] + " " + fillin
        elif spicemanip(bot, fillin, 1).lower() in botcom.dotcommand_dict["reasonhandle"] and not ignorefillin:
            if spicemanip(bot, fillin, 1).lower() != botcom.dotcommand_dict["reasonhandle"][0]:
                botcom.triggerargsarray = spicemanip(bot, botcom.triggerargsarray, '2+', 'list')
                fillin = botcom.dotcommand_dict["reasonhandle"][0] + " " + spicemanip(bot, botcom.triggerargsarray, 0)

    if not isinstance(reply, list):
        reply = [reply]

    for rply in reply:
        rply = rply.replace("$blank", fillin)
        rply = rply.replace("$target", target)
        rply = rply.replace("$instigator", botcom.instigator)
        rply = rply.replace("$channel", botcom.channel_current)
        if rply.startswith("time.sleep"):
            eval(rply)
        elif rply.startswith("*a "):
            rply = rply.replace("*a ", "")
            osd(bot, botcom.channel_current, 'action', rply)
        else:
            osd(bot, botcom.channel_current, 'say', rply)


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
    targetgood = {"targetgood": True, "error": "None"}

    targetgoodconsensus = []

    # cannot target bots
    if target in bot.memory["botdict"]["tempvals"]['bots_list']:
        targetgoodconsensus.append(nick_actual(bot, target) + " is a bot and cannot be targeted.")

    # Not a valid user
    if target not in bot.memory["botdict"]["users"].keys():
        targetgoodconsensus.append("I don't know who that is.")

    # User offline
    if target not in bot.memory["botdict"]["tempvals"]['all_current_users']:
        targetgoodconsensus.append("It looks like " + nick_actual(bot, target) + " is offline right now!")

    if not botcom.channel_current.startswith('#') and target != botcom.instigator:
        targetgoodconsensus.append("Leave " + nick_actual(bot, target) + " out of this private conversation!")

    if target in bot.memory["botdict"]["tempvals"]['all_current_users'] and target not in bot.memory["botdict"]["tempvals"]['channels_list'][botcom.channel_current]['current_users']:
        targetgoodconsensus.append("It looks like " + nick_actual(bot, target) + " is online right now, but in a different channel.")

    if targetgoodconsensus != []:
        targetgood = {"targetgood": False, "error": targetgoodconsensus[0]}

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
