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
@rule('^\?(.*)')
@rule('(.*)')
"""


@rule('^\?(.*)')
@sopel.module.thread(True)
def mainfunction(bot, trigger):

    # command must start with
    if not str(trigger).startswith(tuple(['?'])):
        return

    botcom = botcom_symbol_trigger(bot, trigger)

    # Bots block
    if bot_check_inlist(bot, botcom.instigator, [bot.nick]):
        return

    execute_main(bot, trigger, botcom)
    botdict_save(bot)


def execute_main(bot, trigger, botcom):

    commands_list = dict()
    for commandstype in ['dict_commands', 'module_commands', 'nickname_commands']:
        for com in bot.memory[commandstype].keys():
            if com not in commands_list.keys():
                commands_list[com] = bot.memory[commandstype][com]

    # command issued, check if valid
    botcom.querycommand = spicemanip(bot, botcom.triggerargsarray, 1).lower()[1:]
    if len(botcom.querycommand) == 1:
        commandlist = []
        for command in commands_list.keys():
            if command.lower().startswith(botcom.querycommand):
                commandlist.append(command)
        if commandlist == []:
            return osd(bot, botcom.instigator, 'say', "No commands match " + str(botcom.querycommand) + ".")
        else:
            return osd(bot, botcom.instigator, 'say', "The following commands match " + str(botcom.querycommand) + ": " + spicemanip(bot, commandlist, 'andlist') + ".")

    elif botcom.querycommand.endswith(tuple(["+"])):
        botcom.querycommand = botcom.querycommand[:-1]
        if botcom.querycommand not in commands_list.keys():
            return osd(bot, botcom.instigator, 'say', "The " + str(botcom.querycommand) + " does not appear to be valid.")
        realcom = botcom.querycommand
        if "aliasfor" in commands_list[botcom.querycommand].keys():
            realcom = commands_list[botcom.querycommand]["aliasfor"]
        validcomlist = commands_list[realcom]["validcoms"]
        return osd(bot, botcom.instigator, 'say', "The following commands match " + str(botcom.querycommand) + ": " + spicemanip(bot, validcomlist, 'andlist') + ".")

    elif botcom.querycommand.endswith(tuple(['?'])):
        botcom.querycommand = botcom.querycommand[:-1]
        sim_com, sim_num = [], []
        for com in commands_list.keys():
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

    elif botcom.querycommand in commands_list.keys():
        return osd(bot, botcom.instigator, 'say', "The following commands match " + str(botcom.querycommand) + ": " + str(botcom.querycommand) + ".")

    elif not botcom.querycommand:
        return

    else:
        commandlist = []
        for command in commands_list.keys():
            if command.lower().startswith(botcom.querycommand):
                commandlist.append(command)
        if commandlist == []:
            return osd(bot, botcom.instigator, 'say', "No commands match " + str(botcom.querycommand) + ".")
        else:
            return osd(bot, botcom.instigator, 'say', "The following commands match " + str(botcom.querycommand) + ": " + spicemanip(bot, commandlist, 'andlist') + ".")
