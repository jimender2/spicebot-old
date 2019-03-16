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
shareddir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(shareddir)
from BotShared import *

# Ensure Encoding
reload(sys)
sys.setdefaultencoding('utf-8')


@event('JOIN')
@rule('.*')
@sopel.module.thread(True)
def bot_join_hub(bot, trigger):

    # don't run jobs if not ready
    while not bot_startup_requirements_met(bot, ["connected", "botdict", "server", "channels", "users"]):
        pass

    # botcom dynamic Class
    botcom = class_create('botcom')
    botcom.default = 'botcom'

    # what time was this triggered
    botcom.timestart = time.time()

    # instigator
    botcom.instigator = str(trigger.nick)
    botcom.instigator_hostmask = str(trigger.hostmask)
    botcom.instigator_user = str(trigger.user)

    # bot credentials
    botcom.admin = trigger.admin
    botcom.owner = trigger.owner

    # server
    botcom.server = bot.memory["botdict"]["tempvals"]['server']

    # channel
    botcom.channel_current = str(trigger.sender).lower()
    botcom.channel_priv = trigger.is_privmsg

    # Bots block
    if bot_check_inlist(bot, botcom.instigator, [bot.nick]):
        return

    # does not apply to bots
    if "altbots" in bot.memory:
        if bot_check_inlist(bot, botcom.instigator, bot.memory["altbots"].keys()):
            return

    # database entry for user
    if botcom.instigator not in bot.memory["botdict"]["users"].keys():
        bot.memory["botdict"]["users"][botcom.instigator] = dict()

    # channel list
    if botcom.instigator not in bot.memory["botdict"]["tempvals"]['servers_list'][str(botcom.server)]['channels_list'][botcom.channel_current]['current_users']:
        bot.memory["botdict"]["tempvals"]['servers_list'][str(botcom.server)]['channels_list'][botcom.channel_current]['current_users'].append(botcom.instigator)

    # all current users and offline users
    if botcom.instigator not in bot.memory["botdict"]["tempvals"]["servers_list"][str(botcom.server)]['all_current_users']:
        bot.memory["botdict"]["tempvals"]["servers_list"][str(botcom.server)]['all_current_users'].append(botcom.instigator)

    userprivdict = dict()
    try:
        userprivdict[botcom.instigator] = bot.privileges[botcom.channel_current][botcom.instigator] or 0
    except KeyError:
        userprivdict[botcom.instigator] = 0
    for privtype in ['VOICE', 'HALFOP', 'OP', 'ADMIN', 'OWNER']:
        privstring = str("chan" + privtype.lower() + "s")
        if userprivdict[botcom.instigator] == eval(privtype):
            if botcom.instigator not in bot.memory["botdict"]["tempvals"]['servers_list'][str(botcom.server)]['channels_list'][botcom.channel_current][privstring]:
                bot.memory["botdict"]["tempvals"]['servers_list'][str(botcom.server)]['channels_list'][botcom.channel_current][privstring].append(botcom.instigator)
        elif userprivdict[botcom.instigator] >= eval(privtype) and privtype == 'OWNER':
            if botcom.instigator not in bot.memory["botdict"]["tempvals"]['servers_list'][str(botcom.server)]['channels_list'][botcom.channel_current][privstring]:
                bot.memory["botdict"]["tempvals"]['servers_list'][str(botcom.server)]['channels_list'][botcom.channel_current][privstring].append(botcom.instigator)
        else:
            if botcom.instigator in bot.memory["botdict"]["tempvals"]['servers_list'][str(botcom.server)]['channels_list'][botcom.channel_current][privstring]:
                bot.memory["botdict"]["tempvals"]['servers_list'][str(botcom.server)]['channels_list'][botcom.channel_current][privstring].remove(botcom.instigator)
