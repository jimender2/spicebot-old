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


@nickname_commands('modules')
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
