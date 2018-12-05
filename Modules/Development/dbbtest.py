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


@sopel.module.commands('dbbtest')
def mainfunctionnobeguine(bot, trigger):

    botcom = bot_module_prerun(bot, trigger)
    if not botcom.modulerun:
        return

    if not botcom.multiruns:
        execute_main(bot, trigger, botcom)
    else:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, botcom.triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            botcom.triggerargsarray = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, botcom)

    botdict_save(bot)


def execute_main(bot, trigger, botcom):
    bot.say("DBB Testing")

    # don't run jobs if not ready
    while not bot_startup_requirements_met(bot, ["botdict", "bot_info"]):
        pass

    # modulecount = 0
    # bot.memory["botdict"]["tempvals"]['module_commands'] = dict()

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
        # modulecount += 1
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
                    bot.say(str(curr_commands))

    return
    bot.memory["botdict"]["tempvals"]['module_count'] = modulecount

    # Command Nicks neet to be registered
    for nickcom in valid_botnick_commands.keys():
        bot.memory["botdict"]["tempvals"]['module_commands'][str(bot.nick) + " " + nickcom] = dict()
    nickcomdir = bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]["directory_main"] + "/Modules/BotCore/Nick_Commands/"
    nickcomfiles = len(fnmatch.filter(os.listdir(nickcomdir), '*.py'))
    bot.memory["botdict"]["tempvals"]['module_count'] += int(nickcomfiles)

    bot_startup_requirements_set(bot, "modules")
