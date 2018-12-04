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


@event('KICK')
@rule('.*')
@sopel.module.thread(True)
def botcom_player_return(bot, trigger):

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
    botcom.channel_current = str(trigger.sender)
    botcom.channel_priv = trigger.is_privmsg

    # Bots block
    if bot_check_inlist(bot, botcom.instigator, [bot.nick]):
        return

    # target user
    botcom.target = str(trigger.args[1])

    # database entry for user
    if botcom.target not in bot.memory["botdict"]["users"].keys():
        bot.memory["botdict"]["users"][botcom.target] = dict()

    # channel list
    if botcom.target in bot.memory["botdict"]["tempvals"]['servers_list'][str(botcom.server)]['channels_list'][botcom.channel_current]['current_users']:
        bot.memory["botdict"]["tempvals"]['servers_list'][str(botcom.server)]['channels_list'][botcom.channel_current]['current_users'].remove(botcom.target)

    # status
    for status in ['chanops', 'chanhalfops', 'chanvoices', 'chanowners', 'chanadmins', 'current_users']:
        if botcom.target in bot.memory["botdict"]["tempvals"]['servers_list'][str(botcom.server)]['channels_list'][botcom.channel_current][status]:
            bot.memory["botdict"]["tempvals"]['servers_list'][str(botcom.server)]['channels_list'][botcom.channel_current][status].remove(botcom.target)

    online = False
    onlineconsensus = []
    for channel in bot.memory["botdict"]["tempvals"]['servers_list'][str(botcom.server)]['channels_list'].keys():
        if botcom.instigator in bot.memory["botdict"]["tempvals"]['servers_list'][str(botcom.server)]['channels_list'][channel]['current_users']:
            onlineconsensus.append("True")
        else:
            onlineconsensus.append("False")

    if 'True' not in onlineconsensus:
        online = False

    if not online:

        if botcom.instigator in bot.memory["botdict"]["tempvals"]["servers_list"][str(botcom.server)]['all_current_users']:
            bot.memory["botdict"]["tempvals"]["servers_list"][str(botcom.server)]['all_current_users'].remove(botcom.instigator)
