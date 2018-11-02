#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel.module
from sopel.module import commands, nickname_commands, rule, priority, example, OP, ADMIN, VOICE, event, rule
import sopel
from sopel import module, tools
import re
import datetime
import git
import ConfigParser
import os
import sys
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *

GITWIKIURL = "https://github.com/SpiceBot/SpiceBot/wiki"

# TODO add a notification of traceback errors
# TODO add warn functionality
# TODO channel and user commands

"""
# bot.nick do this
"""


@nickname_commands('modules', 'cd', 'dir', 'gitpull')
@sopel.module.thread(True)
def bot_command_hub(bot, trigger):
    triggerargsarray = spicemanip(bot, trigger.group(0), 'create')
    triggerargsarray = spicemanip(bot, triggerargsarray, '2+')
    triggerargsarray = spicemanip(bot, triggerargsarray, 'create')
    bot_command_process(bot, trigger, triggerargsarray)


def bot_command_process(bot, trigger, triggerargsarray):

    # Dyno Classes
    botcom = class_create('bot')
    instigator = class_create('instigator')
    botcom.instigator = trigger.nick

    # time
    botcom.now = time.time()

    # User
    botcom = bot_command_users(bot, botcom)

    # Channels
    botcom = bot_command_channels(bot, botcom, trigger)

    # Command Used
    botcom.command_main = spicemanip(bot, triggerargsarray, 1)
    if botcom.command_main in triggerargsarray:
        triggerargsarray.remove(botcom.command_main)
    if botcom.command_main == 'help':
        botcom.command_main = 'docs'
    botcom.triggerargsarray = triggerargsarray
    bot_command_function_run = str('bot_command_function_' + botcom.command_main.lower() + '(bot,trigger,botcom,instigator)')
    eval(bot_command_function_run)


"""
Commands
"""


def bot_command_function_gitpull(bot, trigger, botcom, instigator):

    botcom.directory = get_database_value(bot, bot.nick, 'current_admin_dir') or os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    osd(bot, botcom.channel_current, 'say', "attempting to git pull " + botcom.directory)
    g = git.cmd.Git(botcom.directory)
    g.pull()


def bot_command_function_dir(bot, trigger, botcom, instigator):

    if botcom.instigator not in botcom.opadmin:
        osd(bot, botcom.instigator, 'notice', "You are unauthorized to use this function.")
        return

    botcom.directory = get_database_value(bot, bot.nick, 'current_admin_dir') or os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    botcom = bot_list_directory(bot, botcom)
    if botcom.directory == []:
        osd(bot, botcom.channel_current, 'say', "It appears this directory is empty.")
        return
    displaymsgarray = []
    displaymsgarray.append("Current files located in " + str(botcom.directory) + " :")
    for filename, filefoldertype in zip(botcom.directory_listing, botcom.filefoldertype):
        displaymsgarray.append(str("["+filefoldertype.title()+"] ")+str(filename))
    osd(bot, botcom.channel_current, 'say', displaymsgarray)


def bot_command_function_cd(bot, trigger, botcom, instigator):

    if botcom.instigator not in botcom.opadmin:
        osd(bot, botcom.instigator, 'notice', "You are unauthorized to use this function.")
        return

    validfolderoptions = ['..', 'reset']
    botcom.directory = get_database_value(bot, bot.nick, 'current_admin_dir') or os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
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

    set_database_value(bot, bot.nick, 'current_admin_dir', str(movepath))

    osd(bot, botcom.channel_current, 'say', "Directory Changed to : " + str(movepath))


def bot_command_function_modules(bot, trigger, botcom, instigator):

    # Channel
    channeltarget = spicemanip(bot, [x for x in botcom.triggerargsarray if x.startswith('#')], 1)
    if not channeltarget:
        if botcom.channel_current.startswith('#'):
            channeltarget = botcom.channel_current
        else:
            osd(bot, botcom.instigator, 'notice', "You must specify a valid channel.")
            return

    # SubCommand used
    valid_subcommands = ['enable', 'disable', 'list', 'count']
    subcommand = spicemanip(bot, [x for x in botcom.triggerargsarray if x in valid_subcommands], 1) or 'list'

    bot_visible_coms = []
    for cmds in bot.command_groups.items():
        for cmd in cmds:
            if str(cmd).endswith("]"):
                for x in cmd:
                    bot_visible_coms.append(x)

    bot_enabled_coms = get_database_value(bot, channeltarget, 'modules_enabled') or []

    if subcommand == 'count':
        osd(bot, botcom.channel_current, 'say', 'There are currently ' + str(len(bot_visible_coms)) + ' custom modules installed.')
        return

    if subcommand == 'list':
        botmessagearray = []
        botmessagearray.append("This is a listing of modules that I can see (E=Enabled, A=Available):")
        for command in bot_visible_coms:
            if command in bot_enabled_coms:
                botmessagearray.append(command+"[E]")
            else:
                botmessagearray.append(command+"[A]")
        osd(bot, botcom.instigator, 'notice', botmessagearray)

    # Enable/Disable
    if subcommand == 'enable' or subcommand == 'disable':

        if botcom.instigator not in botcom.opadmin:
            osd(bot, botcom.instigator, 'notice', "You are unauthorized to use this function.")
            return

        module_adjust = spicemanip(bot, [x for x in botcom.triggerargsarray if x in bot_visible_coms or x == 'all'], 1) or 'no_module'
        if module_adjust == 'no_module':
            osd(bot, botcom.instigator, 'notice', "What module do you want to "+str(subcommand)+" for " + channeltarget + "?")
            return

        if module_adjust in bot_enabled_coms and subcommand == 'enable' and module_adjust != 'all':
            osd(bot, botcom.instigator, 'notice', "It looks like "+str(module_adjust)+" is already "+subcommand.lower()+"d for " + channeltarget + "?")
            return

        if module_adjust not in bot_enabled_coms and subcommand == 'disable' and module_adjust != 'all':
            osd(bot, botcom.instigator, 'notice', "It looks like "+str(module_adjust)+" is already "+subcommand.lower()+"d for " + channeltarget + "?")
            return

        if module_adjust == 'all':
            modulesadjustarray = bot_visible_coms
        else:
            modulesadjustarray = [module_adjust]

        if subcommand == 'enable':
            adjust_database_array(bot, channeltarget, modulesadjustarray, 'modules_enabled', 'add')
        else:
            adjust_database_array(bot, channeltarget, modulesadjustarray, 'modules_enabled', 'del')
        osd(bot, botcom.channel_current, 'say', module_adjust + " command(s) should now be "+str(subcommand)+"d for " + channeltarget + ".")


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
