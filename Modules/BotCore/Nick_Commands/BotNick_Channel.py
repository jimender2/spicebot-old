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


comdict = {
            "author": "deathbybandaid",
            "contributors": [],
            "description": "",
            'privs': [],
            "example": "",
            "exampleresponse": "",
            }


"""
This will display bot channels
"""


@nickname_commands('channel')
@sopel.module.thread(True)
def bot_command_hub(bot, trigger):

    botcom = botcom_nick(bot, trigger)

    # Bots block
    if bot_check_inlist(bot, botcom.instigator, [bot.nick]):
        return

    if not bot_permissions_check(bot, botcom):
        return osd(bot, botcom.instigator, 'notice', "I was unable to process this Bot Nick command due to privilege issues.")

    # SubCommand used
    valid_subcommands = ['list', 'op', 'hop', 'voice', 'owner', 'admin', 'users']
    subcommand = spicemanip(bot, [x for x in botcom.triggerargsarray if x.lower() in valid_subcommands], 1) or 'list'
    if subcommand in botcom.triggerargsarray:
        botcom.triggerargsarray.remove(subcommand)
    subcommand = subcommand.lower()

    # list channels
    if subcommand == 'list':
        chanlist = spicemanip(bot, bot.memory["botdict"]["tempvals"]['servers_list'][botcom.server]['channels_list'].keys(), 'andlist')
        osd(bot, botcom.channel_current, 'say', "You can find me in " + chanlist)
        return

    # Channel
    targetchannels = []
    if botcom.triggerargsarray == []:
        if not botcom.channel_priv:
            targetchannels.append(botcom.channel_current)
        else:
            osd(bot, botcom.instigator, 'notice', "You must specify a valid channel.")
            return
    elif 'all' in botcom.triggerargsarray:
        for targetchan in bot.memory["botdict"]["tempvals"]['servers_list'][botcom.server]['channels_list'].keys():
            targetchannels.append(targetchan)
    else:
        for targetchan in botcom.triggerargsarray:
            if targetchan in bot.memory["botdict"]["tempvals"]['servers_list'][botcom.server]['channels_list'].keys():
                targetchannels.append(targetchan)

    dispmsg = []

    # OP list
    if subcommand.lower() == 'op':
        for channeltarget in targetchannels:
            if bot.memory["botdict"]["tempvals"]['servers_list'][botcom.server]['channels_list'][channeltarget]['chanops'] == []:
                dispmsg.append("There are no Channel Operators for " + str(channeltarget))
            else:
                oplist = spicemanip(bot, bot.memory["botdict"]["tempvals"]['servers_list'][botcom.server]['channels_list'][channeltarget]['chanops'], 'andlist')
                dispmsg.append("Channel Operators for " + str(channeltarget) + "  are: " + oplist)
        osd(bot, botcom.instigator, 'notice', spicemanip(bot, dispmsg, 'andlist'))
        return

    # HOP list
    if subcommand.lower() == 'hop':
        for channeltarget in targetchannels:
            if bot.memory["botdict"]["tempvals"]['servers_list'][botcom.server]['channels_list'][channeltarget]['chanhalfops'] == []:
                dispmsg.append("There are no Channel Half Operators for " + str(channeltarget))
            else:
                hoplist = spicemanip(bot, bot.memory["botdict"]["tempvals"]['servers_list'][botcom.server]['channels_list'][channeltarget]['chanhalfops'], 'andlist')
                dispmsg.append("Channel Half Operators for " + str(channeltarget) + "  are: " + hoplist)
        osd(bot, botcom.instigator, 'notice', spicemanip(bot, dispmsg, 'andlist'))
        return

    # Voice List
    if subcommand.lower() == 'voice':
        for channeltarget in targetchannels:
            if bot.memory["botdict"]["tempvals"]['servers_list'][botcom.server]['channels_list'][channeltarget]['chanvoices'] == []:
                dispmsg.append("There are no Channel VOICE for " + str(channeltarget))
            else:
                voicelist = spicemanip(bot, bot.memory["botdict"]["tempvals"]['servers_list'][botcom.server]['channels_list'][channeltarget]['chanvoices'], 'andlist')
                dispmsg.append("Channel VOICE for " + str(channeltarget) + " are: " + voicelist)
        osd(bot, botcom.instigator, 'notice', spicemanip(bot, dispmsg, 'andlist'))
        return

    # owner List
    if subcommand.lower() == 'owner':
        for channeltarget in targetchannels:
            if bot.memory["botdict"]["tempvals"]['servers_list'][botcom.server]['channels_list'][channeltarget]['chanowners'] == []:
                dispmsg.append("There are no Channel OWNER for " + str(channeltarget))
            else:
                ownerlist = spicemanip(bot, bot.memory["botdict"]["tempvals"]['servers_list'][botcom.server]['channels_list'][channeltarget]['chanowners'], 'andlist')
                dispmsg.append("Channel OWNER for " + str(channeltarget) + " are: " + ownerlist)
        osd(bot, botcom.instigator, 'notice', spicemanip(bot, dispmsg, 'andlist'))
        return

    # admin List
    if subcommand.lower() == 'admin':
        for channeltarget in targetchannels:
            if bot.memory["botdict"]["tempvals"]['servers_list'][botcom.server]['channels_list'][channeltarget]['chanadmins'] == []:
                dispmsg.append("There are no Channel ADMIN for " + str(channeltarget))
            else:
                adminlist = spicemanip(bot, bot.memory["botdict"]["tempvals"]['servers_list'][botcom.server]['channels_list'][channeltarget]['chanadmins'], 'andlist')
                dispmsg.append("Channel ADMIN for " + str(channeltarget) + " are: " + adminlist)
        osd(bot, botcom.instigator, 'notice', spicemanip(bot, dispmsg, 'andlist'))
        return

    # Users List
    if subcommand.lower() == 'users':
        for channeltarget in targetchannels:
            if bot.memory["botdict"]["tempvals"]['servers_list'][botcom.server]['channels_list'][channeltarget]['current_users'] == []:
                dispmsg.append("There are no Channel users for " + str(channeltarget))
            else:
                userslist = spicemanip(bot, bot.memory["botdict"]["tempvals"]['servers_list'][botcom.server]['channels_list'][channeltarget]['current_users'], 'andlist')
                dispmsg.append("Channel users for " + str(channeltarget) + " are: " + userslist)
        osd(bot, botcom.instigator, 'notice', spicemanip(bot, dispmsg, 'andlist'))
        return
