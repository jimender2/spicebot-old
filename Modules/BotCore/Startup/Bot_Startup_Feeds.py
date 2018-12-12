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


"""
This Cycles through all of the dictionary commands
"""


@event('001')
@rule('.*')
@sopel.module.thread(True)
def bot_startup_feeds(bot, trigger):

    # don't run jobs if not ready
    while not bot_startup_requirements_met(bot, ["botdict", "bot_info", "txt_files"]):
        pass

    feed_configs(bot)

    bot_startup_requirements_set(bot, "feeds")


# Command configs
def feed_configs(bot):

    feedcount, feedopenfail = 0, 0
    filescan = []
    bot.memory["botdict"]["tempvals"]['feeds'] = dict()
    bot.memory["botdict"]["tempvals"]['feeds_loaded'] = []

    quick_coms_path = bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]["directory_main"] + "Modules/Feeds/" + str(bot.nick) + "/"
    if os.path.exists(quick_coms_path) and os.path.isdir(quick_coms_path):
        if not os.path.isfile(quick_coms_path) and len(os.listdir(quick_coms_path)) > 0:
            filescan.append(quick_coms_path)

    if "feeds" in bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]['configuration'].keys():
        if "extra" in bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]['configuration']["feeds"].keys():
            if "," not in str(bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]['configuration']["feeds"]["extra"]):
                extradirs = [str(bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]['configuration']["feeds"]["extra"])]
            else:
                extradirs = str(bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]['configuration']["feeds"]["extra"]).split(",")
            for extra in extradirs:
                quick_coms_path_extra = bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]["directory_main"] + "Modules/Feeds/" + str(extra) + "/"
                if os.path.exists(quick_coms_path_extra) and os.path.isdir(quick_coms_path_extra):
                    if not os.path.isfile(quick_coms_path_extra) and len(os.listdir(quick_coms_path_extra)) > 0:
                        filescan.append(quick_coms_path_extra)

    # proceed with file iteration
    for directory in filescan:

        # iterate over organizational folder
        for quick_coms_type in os.listdir(directory):
            coms_type_file_path = os.path.join(directory, quick_coms_type)
            if os.path.exists(coms_type_file_path) and not os.path.isfile(coms_type_file_path) and len(os.listdir(coms_type_file_path)) > 0:

                # iterate over files within
                for comconf in os.listdir(coms_type_file_path):
                    comconf_file_path = os.path.join(coms_type_file_path, comconf)

                    if os.path.isfile(comconf_file_path):

                        # check if command file is already in the list
                        if comconf not in bot.memory["botdict"]["tempvals"]['feeds_loaded']:
                            bot.memory["botdict"]["tempvals"]['feeds_loaded'].append(comconf)

                            # Read dictionary from file, if not, enable an empty dict
                            filereadgood = True
                            inf = codecs.open(os.path.join(coms_type_file_path, comconf), "r", encoding='utf-8')
                            infread = inf.read()
                            try:
                                dict_from_file = eval(infread)
                            except Exception as e:
                                filereadgood = False
                                stderr("Error loading feed %s: %s (%s)" % (comconf, e, comconf_file_path))
                                dict_from_file = dict()
                            # Close File
                            inf.close()

                            if filereadgood and isinstance(dict_from_file, dict):

                                feedcount += 1

                                if "type" not in dict_from_file.keys():
                                    dict_from_file["type"] = quick_coms_type

                                if "displayname" not in dict_from_file.keys():
                                    dict_from_file["displayname"] = comconf

                                if "url" not in dict_from_file.keys():
                                    dict_from_file["url"] = None

                                if comconf not in bot.memory["botdict"]["tempvals"]['feeds'].keys():
                                    bot.memory["botdict"]["tempvals"]['feeds'][comconf] = dict_from_file
                            else:
                                feedopenfail += 1
    if feedcount > 1:
        stderr('\n\nRegistered %d feed files,' % (feedcount))
        stderr('%d feed files failed to load\n\n' % feedopenfail)
    else:
        stderr("Warning: Couldn't load any feed files")

    bot.memory["botdict"]["tempvals"]['feed_count'] = feedcount
