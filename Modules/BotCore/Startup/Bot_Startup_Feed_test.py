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

    dirdict = {
                "name": "feeds",
                "botmemname": "feeds",
                "dirname": "Feeds",
                }

    configs_dir_read(bot, dirdict)


def configs_dir_read(bot, dirdict):

    if "name" not in dirdict.keys():
        return

    if "botmemname" not in dirdict.keys():
        dirdict['botmemname'] = dirdict['name']

    if "dirname" not in dirdict.keys():
        dirdict['dirname'] = dirdict['botmemname']

    if "configname" not in dirdict.keys():
        dirdict['configname'] = dirdict['botmemname']

    bot_directory_main = str("/home/spicebot/.sopel/" + str(bot.nick) + "/")
    bot_directory_configs = bot_directory_main + "Modules/Configs/" + dirdict['dirname'] + "/"

    if not os.path.exists(bot_directory_configs) or not os.path.isdir(bot_directory_configs):
        bot.msg("#spicebottest", "path failed completely")
        return

    bot_config_dir = str(bot_directory_main + "System-Files/Configs/" + bot.memory["botdict"]["tempvals"]['servername'] + "/")
    bot_config_file = str(bot_config_dir + str(bot.nick) + ".cfg")

    botconfig = config_file_to_dict(bot, str(config_file))

    filecount, fileopenfail = 0, 0
    dirscan = []

    # Open files within botname dir, check bot config for others
    configlocations = [str(bot.nick)]
    if dirdict['configname'] in botconfig.keys():
        if "extra" in botconfig[dirdict['configname']].keys():
            if "," not in str(botconfig[dirdict['configname']]["extra"]):
                extradirs = [str(botconfig[dirdict['configname']]["extra"])]
            else:
                extradirs = str(botconfig[dirdict['configname']]["extra"]).split(",")
            configlocations.extend(extradirs)

    for confloc in configlocations:
        conf_path = bot_directory_configs + str(confloc) + "/"
        if os.path.exists(conf_path) and os.path.isdir(conf_path):
            if not os.path.isfile(conf_path) and len(os.listdir(conf_path)) > 0:
                dirscan.append(conf_path)

    filesprocess = []

    for directory in dirscan:

        for dir_main_item in os.listdir(directory):

            dir_main_item_path = os.path.join(directory, dir_main_item)

            if os.path.isfile(dir_main_item_path):
                filesprocess.append(dir_main_item_path)

            elif not os.path.isfile(dir_main_item_path):

                for dir_sub_item in os.listdir(dir_main_item_path):

                    dir_sub_item_path = os.path.join(dir_main_item, dir_sub_item)

                    if os.path.isfile(dir_sub_item_path):
                        filesprocess.append(dir_sub_item_path)

    # file dicts
    filedicts = []
    for filepath in filesprocess:

        # Read dictionary from file, if not, enable an empty dict
        filereadgood = True
        inf = codecs.open(filepath, "r", encoding='utf-8')
        infread = inf.read()
        try:
            dict_from_file = eval(infread)
        except Exception as e:
            filereadgood = False
            stderr("Error loading %s %s: %s (%s)" % (dirdict['name'], comconf, e, filepath))
            dict_from_file = dict()
        # Close File
        inf.close()

        if filereadgood and isinstance(dict_from_file, dict):

            filecount += 1

            # current file info
            if "filepath" not in dict_from_file.keys():
                dict_from_file["filepath"] = filepath

            slashsplit = str(filepath).split("/")
            filename = slashsplit[-1]

            if "filename" not in dict_from_file.keys():
                dict_from_file["filename"] = filename

            filedicts.append(dict_from_file)

        else:
            fileopenfail += 1

    if filecount > 1:
        stderr('\n\nRegistered %d %d files,' % (dirdict['name'], filecount))
        stderr('%d %d files failed to load\n\n' % fileopenfail)
    else:
        stderr("Warning: Couldn't load any %d files" % (dirdict['name']))

    return filedicts
