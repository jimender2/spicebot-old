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
Change Directory
"""


@nickname_commands('cd')
@sopel.module.thread(True)
def bot_command_hub(bot, trigger):

    botcom = botcom_nick(bot, trigger)

    # Bots block
    if bot_check_inlist(bot, botcom.instigator, [bot.nick]):
        return

    if not bot_nickcom_run_check(bot, botcom):
        return osd(bot, botcom.instigator, 'notice', "I was unable to process this Bot Nick command due to privilege issues.")

    validfolderoptions = ['..', 'reset']
    botcom.directory = get_nick_value(bot, botcom.instigator, 'temp', 'unsorted', 'current_admin_dir') or bot.memory["botdict"]["tempvals"]["bot_info"][str(bot.nick)]["directory_main"]
    get_nick_value(bot, botcom.instigator, longevity, sortingkey, usekey)
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

    set_nick_value(bot, botcom.instigator, 'temp', 'unsorted', 'current_admin_dir', str(movepath))

    osd(bot, botcom.channel_current, 'say', "Directory Changed to : " + str(movepath))
