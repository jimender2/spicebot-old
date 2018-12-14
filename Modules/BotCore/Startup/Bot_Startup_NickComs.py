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
This counts the python modules
"""


@event('001')
@rule('.*')
@sopel.module.thread(True)
def bot_startup_modules(bot, trigger):
    return

    # don't run jobs if not ready
    while not bot_startup_requirements_met(bot, ["botdict", "bot_info"]):
        pass

    nickcomcount = 0
    bot.memory["botdict"]["tempvals"]['nick_commands'] = dict()

    # Command Nicks neet to be registered
    for nickcom in valid_botnick_commands.keys():
        bot.memory["botdict"]["tempvals"]['nick_commands'][str(bot.nick) + " " + nickcom] = dict()
    nickcomdir = bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]["directory_main"] + "/Modules/BotCore/Nick_Commands/"
    nickcomfiles = len(fnmatch.filter(os.listdir(nickcomdir), '*.py'))
    bot.memory["botdict"]["tempvals"]['module_count'] += int(nickcomfiles)

    filenameslist = []
    for modules in bot.command_groups.items():
        filename = modules[0]
        if filename not in ["coretasks"]:
            filenameslist.append(filename + ".py")

    filepathlist = []
    for directory in bot.config.core.extra:
        for pathname in os.listdir(directory):
            path = os.path.join(directory, pathname)
            if (os.path.isfile(path) and path.endswith('.py') and not path.startswith('_')):
                if pathname in filenameslist:
                    filepathlist.append(str(path))

    for module in filepathlist:
        nickcomcount += 1
        module_file_lines = []
        module_file = open(module, 'r')
        lines = module_file.readlines()
        for line in lines:
            module_file_lines.append(line)
        module_file.close()

        dict_from_file = False
        filelinelist = []

        for line in module_file_lines:

            if str(line).startswith("comdict") and not dict_from_file:
                dict_from_file = str(line).replace("comdict = ", "")

            if str(line).startswith("@"):
                line = str(line)[1:]

                # Commands
                if str(line).startswith(tuple(["commands", "module.commands", "sopel.module.commands"])):
                    line = str(line).split("commands(")[-1]
                    line = str("(" + line)
                    validcoms = eval(str(line))
                    if isinstance(validcoms, tuple):
                        validcoms = list(validcoms)
                    else:
                        validcoms = [validcoms]
                    filelinelist.append(validcoms)

        if not dict_from_file:
            dict_from_file = dict()
        else:
            try:
                dict_from_file = eval(dict_from_file)
            except Exception as e:
                dict_from_file = dict()

        # current file path
        if "filepath" not in dict_from_file.keys():
            dict_from_file["filepath"] = str(module)

        # default command to filename
        if "validcoms" not in dict_from_file.keys():
            dict_from_file["validcoms"] = validcoms

        maincom = dict_from_file["validcoms"][0]
        if len(dict_from_file["validcoms"]) > 1:
            comaliases = spicemanip(bot, dict_from_file["validcoms"], '2+', 'list')
        else:
            comaliases = []

        # the command must have an author
        if "author" not in dict_from_file.keys():
            dict_from_file["author"] = "deathbybandaid"

        if "contributors" not in dict_from_file.keys():
            dict_from_file["contributors"] = []
        if not isinstance(dict_from_file["contributors"], list):
            dict_from_file["contributors"] = [dict_from_file["contributors"]]
        if "deathbybandaid" not in dict_from_file["contributors"]:
            dict_from_file["contributors"].append("deathbybandaid")
        if dict_from_file["author"] not in dict_from_file["contributors"]:
            dict_from_file["contributors"].append(dict_from_file["author"])

        if "hardcoded_channel_block" not in dict_from_file.keys():
            dict_from_file["hardcoded_channel_block"] = []

        bot.memory["botdict"]["tempvals"]['module_commands'][maincom] = dict_from_file
        for comalias in comaliases:
            if comalias not in bot.memory["botdict"]["tempvals"]['module_commands'].keys():
                bot.memory["botdict"]["tempvals"]['module_commands'][comalias] = {"aliasfor": maincom}

    bot.memory["botdict"]["tempvals"]['nickcom_count'] = nickcomcount

    # Command Nicks neet to be registered
    for nickcom in valid_botnick_commands.keys():
        bot.memory["botdict"]["tempvals"]['module_commands'][str(bot.nick) + " " + nickcom] = dict()
    nickcomdir = bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]["directory_main"] + "/Modules/BotCore/Nick_Commands/"
    nickcomfiles = len(fnmatch.filter(os.listdir(nickcomdir), '*.py'))
    bot.memory["botdict"]["tempvals"]['module_count'] += int(nickcomfiles)

    bot_startup_requirements_set(bot, "nickmodules")
