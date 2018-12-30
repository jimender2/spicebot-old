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


@event('MODE')
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
    botcom.channel_current = str(trigger.sender).lower()
    botcom.channel_priv = trigger.is_privmsg

    # Bots block
    if bot_check_inlist(bot, botcom.instigator, [bot.nick]):
        return

    # does not apply to bots
    if "altbots" in bot.memory:
        if bot_check_inlist(bot, botcom.instigator, bot.memory["altbots"].keys()):
            return

    # target
    target = str(trigger.args[-1])

    # Mode set
    modeused = str(trigger.args[1])

    if str(modeused).startswith("-"):
        modetype = 'del'
    elif str(modeused).startswith("+"):
        modetype = 'add'

    if modeused[1:] in mode_dict_alias.keys():

        userprivdict = dict()
        userprivdict[target] = eval(mode_dict_alias[modeused[1:]])

        for privtype in ['VOICE', 'HALFOP', 'OP', 'ADMIN', 'OWNER']:
            privstring = str("chan" + privtype.lower() + "s")
            if modetype == 'add':
                if userprivdict[target] == eval(privtype):
                    if target not in bot.memory["botdict"]["tempvals"]['servers_list'][str(botcom.server)]['channels_list'][botcom.channel_current][privstring]:
                        bot.memory["botdict"]["tempvals"]['servers_list'][str(botcom.server)]['channels_list'][botcom.channel_current][privstring].append(target)
                else:
                    if target in bot.memory["botdict"]["tempvals"]['servers_list'][str(botcom.server)]['channels_list'][botcom.channel_current][privstring]:
                        bot.memory["botdict"]["tempvals"]['servers_list'][str(botcom.server)]['channels_list'][botcom.channel_current][privstring].remove(target)
            elif modetype == 'del':
                if userprivdict[target] == eval(privtype):
                    if target in bot.memory["botdict"]["tempvals"]['servers_list'][str(botcom.server)]['channels_list'][botcom.channel_current][privstring]:
                        bot.memory["botdict"]["tempvals"]['servers_list'][str(botcom.server)]['channels_list'][botcom.channel_current][privstring].remove(target)
                else:
                    if target in bot.memory["botdict"]["tempvals"]['servers_list'][str(botcom.server)]['channels_list'][botcom.channel_current][privstring]:
                        bot.memory["botdict"]["tempvals"]['servers_list'][str(botcom.server)]['channels_list'][botcom.channel_current][privstring].remove(target)
