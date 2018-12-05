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

    # don't run jobs if not ready
    while not bot_startup_requirements_met(bot, ["botdict", "bot_info"]):
        pass

    modulecount = 0
    bot.memory["botdict"]["tempvals"]['module_commands'] = dict()

    filenameslist = []
    for modules in bot.command_groups.items():
        filename = modules[0]
        if filename not in ["coretasks"]:
            filenameslist.append(filename + ".py")
    bot.say(str(filenameslist))

    filepathlist = []
    for directory in bot.config.core.extra:
        for pathname in os.listdir(directory):
            path = os.path.join(directory, pathname)
            if (os.path.isfile(path) and path.endswith('.py') and not path.startswith('_')):
                if pathname in filenameslist:
                    filepathlist.append(str(path))

    for module in filepathlist:
        modulecount += 1
        module_file_lines = []
        module_file = open(module, 'r')
        lines = module_file.readlines()
        for line in lines:
            module_file_lines.append(line)
        module_file.close()

        for line in module_file_lines:
            if str(line).startswith("@"):
                line = str(line)[1:]

                # Commands
                if str(line).startswith(tuple(["commands", "module.commands", "sopel.module.commands"])):
                    line = str(line).split("commands(")[-1]
                    line = str("(" + line)
                    curr_commands = eval(str(line))
                    if isinstance(curr_commands, tuple):
                        curr_commands = list(curr_commands)
                    else:
                        curr_commands = [curr_commands]
                    maincom = None
                    if curr_commands != []:
                        currdict = dict()

                        # current file path
                        if "filepath" not in currdict.keys():
                            currdict["filepath"] = str(module)

                        # default command to filename
                        if "validcoms" not in currdict.keys():
                            currdict["validcoms"] = curr_commands

                        maincom = currdict["validcoms"][0]
                        if len(currdict["validcoms"]) > 1:
                            comaliases = spicemanip(bot, currdict["validcoms"], '2+', 'list')
                        else:
                            comaliases = []

                        # the command must have an author
                        if "author" not in currdict.keys():
                            currdict["author"] = "deathbybandaid"

                        if "contributors" not in currdict.keys():
                            currdict["contributors"] = []
                        if "deathbybandaid" not in currdict["contributors"]:
                            currdict["contributors"].append("deathbybandaid")
                        if currdict["author"] not in currdict["contributors"]:
                            currdict["contributors"].append(currdict["author"])

                        if "hardcoded_channel_block" not in currdict.keys():
                            currdict["hardcoded_channel_block"] = []

                        bot.memory["botdict"]["tempvals"]['module_commands'][maincom] = currdict
                        for comalias in comaliases:
                            if comalias not in bot.memory["botdict"]["tempvals"]['module_commands'].keys():
                                bot.memory["botdict"]["tempvals"]['module_commands'][comalias] = {"aliasfor": maincom}

    bot.memory["botdict"]["tempvals"]['module_count'] = modulecount

    # Command Nicks neet to be registered
    for nickcom in valid_botnick_commands.keys():
        bot.memory["botdict"]["tempvals"]['module_commands'][str(bot.nick) + " " + nickcom] = dict()
    nickcomdir = bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]["directory_main"] + "/Modules/BotCore/Nick_Commands/"
    nickcomfiles = len(fnmatch.filter(os.listdir(nickcomdir), '*.py'))
    bot.memory["botdict"]["tempvals"]['module_count'] += int(nickcomfiles)

    bot_startup_requirements_set(bot, "modules")
